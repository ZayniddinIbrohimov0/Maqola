#include <queue>
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <fstream>
#include <sstream>
#include "common.hpp"
#include "utils.hpp"
using namespace std;

void resetVisited(vector< vector<float> > &visAllotted, vector< vector<float> > row){
    for(int i=0; i<row.size(); i++){
        for(int j=0; j<row[i].size(); j++){
            visAllotted[i][row[i][j]] = 0;
        }
    }
}


int findLeastPathCostIndex(vector<pathCost> pathCostVector){
    float low = 0;
    int ind = 0;
    for(int i=0; i<pathCostVector.size(); i++){
        if(pathCostVector[i].cost < low){
            low = pathCostVector[i].cost;
            ind = i;
        }
    }
    return ind;
}



// using struct in place of complicated pairs
struct LeastCostMethodCompare {
    bool operator()(pair< pair<float, float>, float> a, pair< pair<float, float>, float> b){
        if(a.second == b.second){
           if(a.first.first == b.first.first){
                return a.first.second > b.first.second;
            }else{
                return a.first.first > b.first.first;
            }
        }else{
            return a.second > b.second;
        }
    }
};

Ans LeastCostMethod(vector< vector<float> > costs, vector<float> supply, vector<float> demand){
    int i = 0,j = 0;
    int s = costs.size();
    int d = costs[0].size();
    Ans ans(s,d);
    vector <bool> visRow (s,0), visCol (d,0);
    priority_queue< pair< pair<float, float>, float>, vector< pair< pair<float, float>, float> >, LeastCostMethodCompare > pq;
    for(i=0; i<s; i++){
        for(j=0; j<d; j++){
            pq.push( make_pair( make_pair(i,j), costs[i][j] ));
        }
    }

    while(!pq.empty()){
        auto a = pq.top();
        pq.pop();
        i = a.first.first;
        j = a.first.second;
        if( !visRow[i] && !visCol[j] ){  // check && or ||
            if(supply[i] <= demand[j]){
                ans.totalCost += costs[i][j] * supply[i];
                ans.allocated[i][j] = supply[i];
                demand[j] -= supply[i];
                supply[i] = 0;
                visRow[i] = 1;
                // i++;
            }else{
                ans.totalCost += costs[i][j] * demand[j];
                ans.allocated[i][j] = demand[j];
                supply[i] -= demand[j];
                demand[j] = 0;
                visCol[j] = 1;
                // j++;
            }    
        }
    }
    return ans;
}


void calcUV(int s, int d, vector< vector<float> > costs, vector< vector<float> > row, vector< vector<float> > col, 
            int r, int c, vector<bool> visRow, vector<bool> visCol, 
            vector<float> &u, vector<float> &v){

    if(r != -1 and visRow[r] == false){
        // row
        visRow[r] = true;
        for(int i=0; i<row[r].size(); i++){
            v[row[r][i]] = costs[r][row[r][i]] - u[r];
            calcUV(s, d, costs, row, col, -1, row[r][i], visRow, visCol, u, v);
        }        
    }else if(c != -1 and visCol[c] == false){
        // col
        visCol[c] = true;
        for(int i=0; i<col[c].size(); i++){
            u[col[c][i]] = costs[col[c][i]][c] - v[c];
            calcUV(s, d, costs, row, col, col[c][i], -1, visRow, visCol, u, v);
        }
    }
    return;
}

Ans MODIMethod(vector< vector<float> > costs, vector<float> supply, vector<float> demand){
    int s = costs.size();
    int d = costs[0].size();
    Ans ans = LeastCostMethod(costs, supply, demand); 

    vector<float> u(s,0);
    vector<float> v(d,0);
    
    vector< vector<float> > row(s);
    vector< vector<float> > col(d);
    vector< vector<float> > c(s, vector<float> (d, 0)); // contains sum and diff values for both allocated and not allocated
  
    int mind = 0, minr = 0, minc = 0; // min difference, row and col corresponding to this difference
    vector< vector<float> > visAllotted(s, vector<float> (d, -1)); // ever changing?
    while(true){
        mind = 0;
        
        vector<bool> visRow(s, false);
        vector<bool> visCol(d, false);
        initRowCol(ans, row, col, s, d);
        calcUV(s, d, costs, row, col, 0, -1, visRow, visCol, u, v);

        for(int i=0; i<s; i++){
            for(int j=0; j<d; j++){
                if(!ans.allocated[i][j]){
                    c[i][j] = costs[i][j] - (u[i] + v[j]); 
                    if(c[i][j] < mind){
                        mind = c[i][j];
                        minr = i;
                        minc = j;
                    }   
                } 
            }
        }
        
        if (mind < 0){
            initVisAllotted(ans, s, d, visAllotted); // can be made easy with pCost values
            // modifying row and col in both
            pathCost pCost;
            pCost.ind[0] = minr;
            pCost.ind[3] = minc;
            pCost.cost = costs[minr][minc];
            bool check = false;
            visAllotted[minr][minc] = 1;
            findClosedPath(ans, costs, s, d, row, col, visAllotted, minr, 1, check, pCost);
            updateAnsForNegativeCostClosedPath(ans, pCost);
        }else{
            break;
        }
            // printAns(ans, s, d);
    }
           
    return ans;
}


Ans SteppingStoneMethod(vector< vector<float> > costs, vector<float> supply, vector<float> demand){
    int s = costs.size();
    int d = costs[0].size();
    Ans ans = LeastCostMethod(costs, supply, demand);
    vector< vector<float> > row(s);
    vector< vector<float> > col(d);
    vector< vector<float> > visAllotted(s, vector<float> (d, -1));
    
    int iter = 0;
    vector<pathCost> pathCostVector;
    while(pathCostVector.size() > 0 or iter == 0){
    
        pathCostVector.clear();
        iter++;
        initVisAllotted(ans, s, d, visAllotted);  // optimize?
        initRowCol(ans, row, col, s, d);
        int temp =0;
        
        for(int i=0; i<s; i++){    
            for(int j=0; j<d; j++){
                if(ans.allocated[i][j]==0){ 
                    // reset to init state
                    resetVisited(visAllotted, row);
                    pathCost pCost;
                    pCost.ind[0] = i;
                    pCost.ind[3] = j;
                    pCost.cost = costs[i][j];
                    
                    bool check = false;
                    visAllotted[i][j] = 1;
                    findClosedPath(ans, costs, s, d, row, col, visAllotted, i, 1, check, pCost);
                    visAllotted[i][j] = -1;
                    
                    // only store negative costs
                    temp++;
                    if(pCost.cost < 0){ 
                        pathCostVector.push_back(pCost);
                    }
                }
            }
        }
        
        if (!pathCostVector.empty()){
            int ind = findLeastPathCostIndex(pathCostVector);
            updateAnsForNegativeCostClosedPath(ans, pathCostVector[ind]);
        }
    }
    return ans;
}

const char* api_costs = "api/costs.txt";
const char* api_demand = "api/demand.txt";
const char* api_offer = "api/offer.txt";
const char* api_rezult_ssm = "api/rezult_ssm.txt";
const char* api_rezult_lcm = "api/rezult_lcm.txt";
const char* api_rezult_modi = "api/rezult_modi.txt";
const char* total_costs = "api/total_costs.txt";

std::vector<float> get_demand_from_file() {
    std::vector<float> demand;
    std::ifstream ifs(api_demand);
    std::string str;
    getline(ifs, str);
    ifs.close();
    
    std::istringstream iss(str);
    float number;
    while (iss >> number) {
        demand.push_back(number);
    }
    return demand;
}

std::vector<float> get_offer_from_file() {
    std::vector<float> offer;
    std::ifstream ifs(api_offer);
    std::string str;
    getline(ifs, str);
    ifs.close();
    
    std::istringstream iss(str);
    float number;
    while (iss >> number) {
        offer.push_back(number);
    }
    return offer;
}


std::vector<std::vector<float>> get_costs_from_file() {
    std::vector<std::vector<float>> matrix;
    std::vector<float> vc;

    std::ifstream ifs(api_costs);
    std::string str;
    
    while (getline(ifs, str)) {
        std::istringstream iss(str);
        float number;
        while (iss >> number)
        {
            vc.push_back(number);
        }
        if (vc.size()) matrix.push_back(vc);
        vc.clear();
    }
    ifs.close();
    return matrix;
}


void set_rezult(Ans answar, const char* api_rezult) {
    std::ofstream ofs(api_rezult);
    for (int i = 0; i < answar.allocated.size(); i++) {
        for (int j = 0; j < answar.allocated[0].size(); j++) {
            if (answar.allocated[i][j] != 0) {
                ofs << answar.allocated[i][j] << " " << i << " " << j << endl;
            }
        }
    }
    ofs.close();
    ofs = ofstream(total_costs);
    ofs << answar.totalCost;
    ofs.close();
}


int main() {
    auto demand = get_demand_from_file();
    auto offer = get_offer_from_file();
    auto costs = get_costs_from_file();

    /** Least Cost Method API creating **/
    set_rezult(LeastCostMethod(costs, offer, demand ), api_rezult_lcm);
    
    
    /** Stepping stone method API creating **/
    set_rezult(SteppingStoneMethod(costs, offer, demand ), api_rezult_ssm);
    
    /** MODI method **/
    set_rezult(MODIMethod(costs, offer, demand ), api_rezult_modi);

    demand.clear();
    offer.clear();
    costs.clear();
    return 0;
}