#include<iostream>
#include <vector>
using namespace std;

// ---------------------------------------
// for all methods/modules
// ---------------------------------------

void printAns(Ans ans, int s, int d){
    cout<<"----Allocated Values---"<<endl;
    for(int i=0; i<s; i++){
        for(int j=0; j<d; j++){
            cout<<ans.allocated[i][j]<<" ";
        }cout<<endl;
    }cout<<ans.totalCost<<endl;
}

// ---------------------------------------
// all structs/funcs below used in SSM, MM
// ---------------------------------------

struct pathCost{
    float ind[4] = {0};
    float cost;
};


void initVisAllotted(Ans ans, int s, int d, vector< vector<float> > &visAllotted){
    for(int i=0; i<s; i++){
        for(int j=0; j<d; j++){
            if(ans.allocated[i][j]){
                visAllotted[i][j] = 0; 
            }else{
                visAllotted[i][j] = -1; 
            }
        }
    }
}


void initRowCol(Ans ans, vector< vector<float> > &row, vector< vector<float> > &col, int s, int d){
    // clear previous values
    for(int i=0; i<s; i++){
        row[i].clear();
    }
    for(int j=0;j<d;j++){
        col[j].clear();
    }

    // init to new values
    for(int i=0; i<s; i++){
        for(int j=0; j<d; j++){
            if(ans.allocated[i][j]){
                row[i].push_back(j);
                col[j].push_back(i);  
            }
        }
    }
}


bool checkVisitedAll(pathCost pCost, vector< vector<float> > visAllotted){
    // returns true if all nodes of closed path are visited
    if(visAllotted[pCost.ind[0]][pCost.ind[3]] == 1 and visAllotted[pCost.ind[0]][pCost.ind[1]] == 1 and 
       visAllotted[pCost.ind[2]][pCost.ind[1]] == 1 and visAllotted[pCost.ind[2]][pCost.ind[3]] == 1 ){
            return true;
    }
    return false;
}


void findClosedPath(Ans ans, vector< vector<float> > costs, int s, int d, 
                    vector< vector<float> > row, vector< vector<float> > col,                   
                    vector< vector<float> > &visAllotted, int I, int pathIndex, bool &check,  // vars modified 
                    pathCost &pCost ){                                                      //output
    
    if(pathIndex == 4){
        if(checkVisitedAll(pCost, visAllotted)){  
            check = true; 
        }
        return;
    }
    if (pathIndex % 2 == 1){
        // row
        for(int i=0; i<row[I].size(); i++){
            if(ans.allocated[I][row[I][i]] and visAllotted[I][row[I][i]]==0){
                visAllotted[I][row[I][i]] = 1; 
                float temp = pCost.ind[pathIndex];
                pCost.ind[pathIndex] = row[I][i];
                findClosedPath(ans, costs, s, d, row, col, visAllotted, row[I][i], pathIndex+1, check, pCost);
                if(check == true){
                    pCost.cost -= costs[I][row[I][i]];
                    return;
                }
                visAllotted[I][row[I][i]] = 0; 
                pCost.ind[pathIndex] = temp;
            }
        }
    }else{
        //col
        for(int i=0; i<col[I].size(); i++){
            if(ans.allocated[col[I][i]][I] and visAllotted[col[I][i]][I]==0){
                visAllotted[col[I][i]][I] = 1; 
                float temp = pCost.ind[pathIndex];
                pCost.ind[pathIndex] = col[I][i];
                findClosedPath(ans, costs, s, d, row, col, visAllotted, col[I][i], pathIndex+1, check, pCost);
                if(check == true){
                    pCost.cost += costs[col[I][i]][I];
                    return;
                }
                visAllotted[col[I][i]][I] = 0; 
                pCost.ind[pathIndex] = temp;
            }
        }
    }
}


void updateAnsForNegativeCostClosedPath(Ans &ans, pathCost pCost){ 
    //update cost for negative least cost closed path
    float x[2];
    float y[2];
    x[0] = pCost.ind[0];
    y[0] = pCost.ind[1];
    x[1] = pCost.ind[2];
    y[1] = pCost.ind[3];
    float minAllocValue = min(ans.allocated[x[0]][y[0]], 
                    ans.allocated[x[1]][y[1]]);
        
    for(int i=0; i<2; i++){
        ans.allocated[x[i]][y[(i+1)%2]] += minAllocValue;
        ans.allocated[x[i]][y[i]] -= minAllocValue;
    }
    ans.totalCost += minAllocValue * pCost.cost;   
}