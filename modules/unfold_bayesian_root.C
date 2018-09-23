void unfold_bayesian_root(int config, int distance, int oneN, int twoN) {

    gRoot->SetBatch(); // don't display the histograms

    // Load the RooUnfold Library
    gSystem->Load("~/Downloads/RooUnfold-1.1.1/libRooUnfold");

    // Get the id for the files we need
    string prior_id, data_id;
    ostringstream convert1, convert2;
    convert1 << 'halo' << config << '_' << distance;
    prior_id = convert1.str()
    convert2 << 'halo' << config << '_' << distance << 'kpc_' << oneN << 'v' << twoN;
    file_id = convert2.str()
    cout << endl << '------------------------------------' << endl;
    cout << 'Now unfolding:' << endl << file_id << endl << endl;

    // Load the Prior
    string prior_location = './priors/';
    string prior_truth = 'prior_' + prior_id + '_truth.txt';
    string prior_obs   = 'prior_' + prior_id + '_observed.txt';

    TTree *tprior_tru = new TTree('tprior_tru','Prior truth');
    TTree *tprior_obs = new TTree('tprior_obs','Prior observed');
    tprior_tru->ReadFile(prior_location+prior_truth,'1nt/D:2nt/D');
    tprior_obs->ReadFile(prior_location+prior_obs,'1no/D:2no/D');


    // Create the response matrix ----------------------------------------------

    // First I need to create a 2D hist with the right dimension
    // Needed to supply dimensions to the response matrix
    int xmax = static_cast<int>(oneN+5*np.sqrt(oneN)+0.5);
    int ymax = static_cast<int>(twoN+5*np.sqrt(twoN)+0.5);  
    TH2D *temp = new TH2D('temp','temp',40,0,xmax,40,0,ymax);

    RooUnfoldResponse response(temp,temp); // Create the response matrix
    temp->Delete(); // we dont need this anymore

    // Fill the response matrix with corresponding pairs of observed,truth

    double tru1n, tru2n, obs1n, obs2n;
    tprior_tru->SetBranchAddress('1nt',&tru1n);
    tprior_tru->SetBranchAddress('2nt',&tru2n);
    tprior_obs->SetBranchAddress('1no',&obs1n);
    tprior_obs->SetBranchAddress('2no',&obs2n);

    for(int i=0; i < tprior_tru->GetEntries(); i++){
        tprior_tru->GetEntry(i);
        tprior_obs->GetEntry(i);
        if (tru1n > xmax) break;
        response.Fill(obs1n,obs2n,tru1n,tru2n);
    }

    // Unfolding ---------------------------------------------------------------

    // Load the data
    string data_location = './data/';
    string data_file = data_location + data_id + '_observed.txt';
    TTree *data = new TTree('data','Observed Data');
    data->ReadFile(data_file,'data1n/D:data2n/D');
    TH2D *data_hist = new TH2D('data_hist','Histogram of observed data',40,0,xmax,40,0,ymax);
    data->Draw('data2n:data1n >> data_hist','','');

    // Unfold the data!
    int iterations = 1;
    // Don't iterate, because that requires an ensemble of detections, 
    // which HALO won't have in real life
    RooUnfoldBayes unfold(&response,data_hist,iterations);
    TH2D* unfolded = (TH2D*) unfold.Hreco();


    // Save the results in a text file
    string unfolded_location = './unfolded_data/';
    string unfolded_file = unfolded_location + file_id + '_unfolded_bayesian.txt';
    ofstream savefile;
    savefile.open(unfolded_file);

    x_unfolded = []
    y_unfolded = []
    int nx = unfolded->GetNbinsX();
    int ny = unfolded->GetNbinsY();
    for (int i=1; i<=nx; i++) {
        for (int j=1; j<=ny; j++) {
            bin = unfolded->GetBin(i,j);
            content = unfolded->GetBinContent(bin);
            xc = unfolded->GetXaxis()->GetBinCenter(i);
            yc = unfolded->GetYaxis()->GetBinCenter(j);
            if content > 0:
                for (int k=0; k<content; k++) {
                    savefile << xc << '       ' << yc << '\n';
                }
        }

    }

    savefile.close();
    
}