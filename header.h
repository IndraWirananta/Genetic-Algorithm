
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

typedef std::string String;
typedef std::vector<String> CSVRow;
typedef CSVRow::const_iterator CSVRowCI;
typedef std::vector<CSVRow> CSVDatabase;
typedef CSVDatabase::const_iterator CSVDatabaseCI;
void readCSV(std::istream &input, CSVDatabase &db);
void display(const CSVRow&);
void display2(const CSVDatabase&);
using namespace std;

int main(){
  std::fstream file("Data.csv", std::ios::in);
  if(!file.is_open()){
    std::cout << "File not found!\n";
    return 1;
  }
  CSVDatabase db;
  readCSV(file, db);
  display2(db);
  cout<<db[4][4]<<endl;
}

void readCSV(std::istream &input, CSVDatabase &db){
  String csvLine;
  // read every line from the stream
  while( std::getline(input, csvLine) ){
    std::istringstream csvStream(csvLine);
    CSVRow csvRow;
    String csvCol;
    // read every element from the line that is seperated by commas
    // and put it into the vector or strings
    while( std::getline(csvStream, csvCol,',') )
      csvRow.push_back(csvCol);
    db.push_back(csvRow);
  }
}
void display(const CSVRow& row){
  if(!row.size())
    return;
  CSVRowCI i=row.begin();
  std::cout<<*(i++);
  for(;i != row.end();++i)
    std::cout<<','<<*i;
}

void display2(const CSVDatabase& db){
  if(!db.size())
    return;
  CSVDatabaseCI i=db.begin();
  for(; i != db.end(); ++i){
    display(*i);
    std::cout<<std::endl;
  }
}
