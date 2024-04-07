#include <iostream>
#include <vector>
using namespace std;

struct Ans {
    Ans(const int m, const int n) : totalCost(0), allocated(m, vector<float>(n,0)){}
    
    float totalCost;
    vector< vector <float> > allocated;
};
