#include <bits/stdc++.h>
#include <sstream>

using namespace std;

class Field {
    public:
        map<string, int> mapField;
};

class Symbol {
    public:
        map<string, Field> mapSymbol;
};

bool compfunction (pair<int, vector<Symbol> > a, pair<int, vector<Symbol> > b) {
    return (a.first < b.first);
}

long long unsigned int sum(vector <pair<int, vector<Symbol> > > data, int start_time, int end_time, string symbol, string field) {

}

int main() {
    vector <pair<int, vector<Symbol> > > vectTicksEngine;
    int nTicks;
    cin >> nTicks;
    ws(cin);
    while(nTicks){
        string input;
        getline(std::cin, input);
    //Tokenizing the given input statement, and storing the corresponding tokens in a vector of strings
        stringstream strInput(input);
        istream_iterator <string> it(strInput);
        istream_iterator <string> endi;
        vector<string> tokenizedInput (it, endi);
        Field tempFld;
        Symbol tempSymb;
    //Iterators for iteration of tokenized vector
        vector<string>::iterator itfName, itfValue;
        itfName= tokenizedInput.begin();
        int timestamp = atoi((*itfName).c_str());
        itfName++;
        string symb = (*itfName);
    //Creating a Symbol
        itfName++;
        while (itfName < tokenizedInput.end()) {
            itfValue = itfName;
            itfValue++;
            tempFld.mapField[*itfName] = atoi((*itfValue).c_str());
            itfName += 2;
        }
        tempSymb.mapSymbol[symb]=tempFld;
        if (!vectTicksEngine.empty() && vectTicksEngine.back().first==timestamp)
            vectTicksEngine.back().second.push_back(tempSymb);
        else {
            vector<Symbol> tempSymbVect;
            tempSymbVect.push_back(tempSymb);
            vectTicksEngine.push_back(make_pair(timestamp,tempSymbVect));
        }
        nTicks--;
    }
    cout << "tickfile completed" << endl;
    // string query;
    // getline(std::cin, query);
    // stringstream queryInput(query);
    // istream_iterator <string> it()
    return 0;
}
