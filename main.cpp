#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
using namespace std;

typedef string integer;
typedef vector<integer> row;
typedef row::const_iterator CSVRowCI;
//typedef vector<CSVRow> CSVDatabase;
//typedef CSVDatabase::const_iterator CSVDatabaseCI;
void readCSV(istream &input, row &db);
void display(const row&);
//void display2(const CSVDatabase&);


int main(){
  fstream file("Book1.csv", ios::in);
  if(!file.is_open()){
    cout << "File not found!\n";
    return 1;
  }
  row db;
  readCSV(file, db);
  //display(db);
  cout<<db[1]<<endl;
}

void readCSV(istream &input, row &db){
  string csvLine;
  while(getline(input,csvLine)){
    db.push_back(csvLine);
  }
}

void display(const row& row2){
  if(!row2.size())
    return;
  CSVRowCI i=row2.begin();
  cout<<*(i++);
  for(;i != row2.end();++i)
    cout<<'\n'<<*i;
}
/*
void display2(const CSVDatabase& db){
  if(!db.size())
    return;
  CSVDatabaseCI i=db.begin();
  for(; i != db.end(); ++i){
    display(*i);
    cout<<endl;
  }
}
*/
