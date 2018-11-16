void unfold_bayesian_root(int config, int distance, int eff, int oneN, int twoN,
                            string prior_truth, string prior_obs) {

    gROOT->SetBatch(); // don't display the histograms

    // Load the RooUnfold Library
    gSystem->Load("~/Downloads/RooUnfold-1.1.1/libRooUnfold");

    // Load the prior
    TTree *tprior_tru = new TTree("tprior_tru","Prior truth");
    TTree *tprior_obs = new TTree("tprior_obs","Prior observed");
    tprior_tru->ReadFile(prior_truth.c_str(),"1nt/D:2nt/D");
    tprior_obs->ReadFile(prior_obs.c_str(),"1no/D:2no/D");


    // Create the response matrix ----------------------------------------------

    // First I need to create a 2D hist with the right dimension
    // Needed to supply dimensions to the response matrix
    int xmax = static_cast<int>(oneN+5*sqrt(oneN)+200);
    int ymax = static_cast<int>(twoN+5*sqrt(twoN)+200); 

    TH2D *temp = new TH2D("temp","temp",40,0,xmax,40,0,ymax);

    RooUnfoldResponse response(temp,temp); // Create the response matrix
    temp->Delete(); // we dont need this anymore

    // Fill the response matrix with corresponding pairs of observed,truth

    double tru1n, tru2n, obs1n, obs2n;
    tprior_tru->SetBranchAddress("1nt",&tru1n);
    tprior_tru->SetBranchAddress("2nt",&tru2n);
    tprior_obs->SetBranchAddress("1no",&obs1n);
    tprior_obs->SetBranchAddress("2no",&obs2n);

    for(int i=0; i < tprior_tru->GetEntries(); i++){
        tprior_tru->GetEntry(i);
        tprior_obs->GetEntry(i);
        if (tru1n > xmax) break;
        response.Fill(obs1n,obs2n,tru1n,tru2n);
    }

    // Unfolding ---------------------------------------------------------------

    // Load the data
    string data_file;
    ostringstream convert3;
    convert3 << "./data/halo" << config << "_"  << distance << "kpc_observed_E" << eff << ".txt";
    data_file = convert3.str();
    TTree *data = new TTree("data","Observed Data");
    data->ReadFile(data_file.c_str(),"data1n/D:data2n/D");
    TH2D *data_hist = new TH2D("data_hist","Histogram of observed data",40,0,xmax,40,0,ymax);
    data->Draw("data2n:data1n >> data_hist","","");

    // Unfold the data!
    int iterations = 1;
    // Don't iterate, because that requires an ensemble of detections, 
    // which HALO won"t have in real life
    RooUnfoldBayes unfold(&response,data_hist,iterations);
    TH2D* unfolded = (TH2D*) unfold.Hreco();


    // Save the results in a text file
    string unfolded_file;
    ostringstream convert4;
    convert4 << "./unfolded_data/halo" << config << "_" << distance << "kpc_unfolded_E" << eff << ".txt";
    unfolded_file = convert4.str();

    ofstream savefile;
    savefile.open(unfolded_file.c_str());

    int nx = unfolded->GetNbinsX();
    int ny = unfolded->GetNbinsY();
    for (int i=1; i<=nx; i++) {
        for (int j=1; j<=ny; j++) {
            int bin = unfolded->GetBin(i,j);
            int content = unfolded->GetBinContent(bin);
            double xc = static_cast<int>(unfolded->GetXaxis()->GetBinCenter(i)+0.5);
            double yc = static_cast<int>(unfolded->GetYaxis()->GetBinCenter(j)+0.5);
            if (content > 0) {
                for (int k=0; k<content; k++) {
                    savefile << xc << "       " << yc << "\n";
                }
            }
        }

    }

    savefile.close();
    
}
