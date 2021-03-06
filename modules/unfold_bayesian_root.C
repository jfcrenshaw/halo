void unfold_bayesian_root(int config, int distance, int oneN, int twoN, int prior) {

    gROOT->SetBatch(); // don't display the histograms

    // Load the RooUnfold Library
    gSystem->Load("~/Downloads/RooUnfold-1.1.1/libRooUnfold");

    // Get the id for the files we need
    string prior_id, data_id;
    ostringstream convert1, convert2;
    convert1 << "halo" << config << "_" << distance << "kpc";
    prior_id = convert1.str();
    convert2 << "halo" << config << "_" << distance << "kpc_" << oneN << "v" << twoN;
    file_id = convert2.str();
    cout << endl << "------------------------------------" << endl;
    cout << "Now unfolding:" << endl << file_id << endl;

    // Load the Prior
    if (prior == 1) {
        // Positive Plane prior
        string unfolding_type = "Positive Plane Prior";
        if (config == 1) {
            string prior_truth = "./priors/prior_positive_plane_truth.txt";
            string prior_obs   = "./priors/prior_positive_plane_observed.txt";
        } else if (config == 2) {
            string prior_truth = "./priors/prior_halo2_positive_plane_truth.txt";
            string prior_obs   = "./priors/prior_halo2_positive_plane_observed.txt";
        }
    }
    else if (prior == 2) {
        // Distance Unknwon prior
        string unfolding_type = "Distance Unknown Prior";
        if (config == 1) {
            string prior_truth = "./priors/prior_distUnknown_truth.txt";
            string prior_obs   = "./priors/prior_distUnknown_observed.txt";
        } else if (config == 2) {
            string prior_truth = "./priors/prior_halo2_distUnknown_truth.txt";
            string prior_obs   = "./priors/prior_halo2_distUnknown_observed.txt";
        } 
    }
    else if (prior == 3) {
        // Distance Known prior
        string unfolding_type = "Distance Known Prior";
        string prior_truth = "./priors/prior_" + prior_id + "_truth.txt";
        string prior_obs   = "./priors/prior_" + prior_id + "_observed.txt";
    }

    cout << "with " << unfolding_type << endl << endl;

    TTree *tprior_tru = new TTree("tprior_tru","Prior truth");
    TTree *tprior_obs = new TTree("tprior_obs","Prior observed");
    tprior_tru->ReadFile(prior_truth.c_str(),"1nt/D:2nt/D");
    tprior_obs->ReadFile(prior_obs.c_str(),"1no/D:2no/D");


    // Create the response matrix ----------------------------------------------

    // First I need to create a 2D hist with the right dimension
    // Needed to supply dimensions to the response matrix
    if (prior == 1) {
        int xmax = tprior_tru->GetMaximum("1nt")+10;
        int ymax = tprior_tru->GetMaximum("2nt")+10;
    }
    else {
        int xmax = static_cast<int>(oneN+5*sqrt(oneN)+100);
        int ymax = static_cast<int>(twoN+5*sqrt(twoN)+100); 
    }

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
    string data_file = "./data/" + file_id + "_observed.txt";
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
    if (prior == 1) {
        // Positive Plane prior
        string unfolded_file = "./unfolded_data/" + file_id + 
                                "_unfolded_bayesian_PP.txt";
    }
    else if (prior == 2) {
        // Distance Unknwon prior
        string unfolded_file = "./unfolded_data/" + file_id + 
                                "_unfolded_bayesian_distUnknown.txt";
    }
    else if (prior == 3) {
        // Distance Known prior
        string unfolded_file = "./unfolded_data/" + file_id + 
                                "_unfolded_bayesian_distKnown.txt";
    }

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
