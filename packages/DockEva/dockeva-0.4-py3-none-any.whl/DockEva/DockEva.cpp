#include <iostream>
#include <string.h>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <cmath>
#include <map>
#include <time.h>
#include <iomanip>
#include <iterator>
#include <cctype>
#include <algorithm>
#include <pybind11/pybind11.h>
using namespace std;
namespace py = pybind11;

/******************************************************************
 * g++ -static -O3 -ffast-math -o DockEva DockEva.cpp
 * g++ -static -O3 -ffast-math -lm -o DockEva DockEva.cpp
 ******************************************************************/ 

const char* VERSION = "20240918";

typedef enum {
	PDB,  // 0
	MOL2, // 1
	SDF   // 2
}INPUT_FILE_TYPE;

typedef enum {
	// MOL2 original definition
	SINGLE,  			// 1 = single
	DOUBLE,  			// 2 = double
	TRIPLE,  			// 3 = triple
	AMIDE,  			// 4 = am (amide)
	AROMATIC, 			// 5 = ar (aromatic)
	DUMMY,  			// 6 = du (dummy) 
	NOTCONNECTED, 		// 7 = nc (not connected)
	DONOTKNOW  		// 8 = do not know
}CHEMICAL_BOND_TYPE;

typedef struct {
	string qaa;
	string taa;
	int qind;
	int tind;
	int qoind;
	int toind;
	double dis2;
}ALIGN_PAIR; 

typedef struct {
	int start_atind;
	int end_atind;
	int roadlen;
}SIMPLE_ROAD;

typedef struct {
	int qind;
	int tind;
	double dis2;
}ALIGN_NODE;

string TOOL_EXE = "DockEva";
 
double g_eps = 1e-9;
double g_inf = 1e+99;
double g_seconds = 259200; // 3*24*60*60 seconds

class CBaseFunc {
	public:
		static void       print_logo();
		static void       print_help(const char* arg); 
		static string     stringTrim(const string& str);
		static void       toUpperString(string &str);
		static string     eraseAll(const string &str, char ch);
		static string     eraseAll(const string &str, const char* arr, int len);
		CBaseFunc();
		virtual    ~CBaseFunc();
		
		static double**   new2Darr(const int& r, const int& c);
		static void       delete2Darr(double** pMtx, const int& r);
		static int*       new1DIntArr(const int& row, const int& val);
		static int**      new2DIntArr(const int& row, const int& col);
		static int**      new2DIntArr(const int& row, const int& col, const int& val);
		static void       delete2DIntArr(const int& n, int ** Arr);
		static bool*      new1Dbool(const int& row);
		static bool**     new2DBoolArr(const int& row, const int& col);
		static bool**     new2DBoolArr(const int& row, const int& col, const bool& val);
		static void       delete2DBoolArr(const int& n, bool ** Arr);
		static int***     new3DIntArr(int row, int col, int thd);
		static int***     new3DIntArr(int row, int col, int thd, int val);
		static void       delete3DIntArr(int row, int col, int*** Arr);
		static string     charVec2String(const vector<char>& vec);
		static vector<string> string2stringVec(const string& str);
		static vector<string> stringSplit(const string& str, const char& spit);
		static vector<string> stringSplit(const string& str, const char& spit1, const char& spit2);
		
		static double d0_of_lsscore(const int& Lnorm);
		
		static double greedySearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec);
		static double __2merExchangedSearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max);
		static double __3merExchangedSearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max); 
		
		static double greedySearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec);
		static double __2merExchangedSearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max);
		static double __3merExchangedSearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max); 
		
		static bool is_same(const vector<char>& a, const vector<char>& b);
		
		static double distance2(const double* a, const double* b);
		
		static unsigned long long factorial(const int& n);
};

class AtomVarDerWaalRadius{
	private:
		map<string, double> vdwRMap;
	public:
		// Can be optimized
		AtomVarDerWaalRadius(){
			// the var der waal radius information is come from "Van der Waals Radii of Elements" (S. S. Batsanov)
			string varDerWaalRadiusStr = "H   1.2 \nHe 1.4 \nLi 2.2 \nBe 1.9 \nB 1.8 \nC 1.7 \nN 1.6 \nO 1.55 \nF 1.5 \nNe 1.5 \nNa 2.4 \nMg 2.2 \nAl 2.1 \nSi 2.1 \nP 1.95 \nS 1.8 \nCl 1.8 \nAr 1.9 \nK 2.8 \nCa 2.4 \nSc 2.3 \nTi 2.15 \nV 2.05 \nCr 2.05 \nMn 2.05 \nFe 2.05 \nCo 2.0 \nNi 2.0 \nCu 2.0 \nZn 2.1 \nGa 2.1 \nGe 2.1 \nAs 2.05 \nSe 1.9 \nBr 1.9 \nKr 2.0 \nRb 2.9 \nSr 2.55 \nY 2.4 \nZr 2.3 \nNb 2.152 \nMo 2.1 \nTc 2.05 \nRu 2.05 \nRh 2.0 \nPd 2.05 \nAg 2.1 \nCd 2.2 \nIn 2.2 \nSn 2.25 \nSb 2.2 \nTe 2.1 \nI 2.1 \nXe 2.2 \nCs 3.0 \nBa 2.7 \nLa 2.5 \nCe 2.35 \nPr 2.39 \nNd 2.29 \nPm 2.36 \nSm 2.29 \nEu 2.33 \nGd 2.37 \nTb 2.21 \nDy 2.29 \nHo 2.16 \nEr 2.35 \nTm 2.27 \nYb 2.42 \nLu 2.21 \nHf 2.25 \nTa 2.2 \nW 2.1 \nRe 2.05 \nOs 2.0 \nIr 2.0 \nPt 2.05 \nAu 2.1 \nHg 2.05 \nTl 2.2 \nPb 2.3 \nBi 2.3 \nPo 2.29 \nAt 2.36 \nRn 2.43 \nFr 2.56 \nRe 2.43 \nRa 2.43 \nAc 2.6 \nTh 2.4 \nPa 2.43 \nU 2.3 \nNp 2.21 \nPu 2.56 \nAm 2.56 \nCm 2.56 \nBk 2.56 \nCf 2.56 \nEs 2.56 \nFm 2.56 \nMd \nNo \nLr \nRf \nDb \nSg \nBh \nHs \nMt \nDs \nRg \nCn \nUut \nUuq \nUup \nUuh \nUus \nUuo ";
	
			vector<string> atomInfos = CBaseFunc::stringSplit(varDerWaalRadiusStr, '\n');
			for (int i = 0; i < atomInfos.size(); i++){
				vector<string> atomRadii = CBaseFunc::stringSplit(atomInfos[i], ' ');
				if (2 == atomRadii.size()){
					string key(atomRadii[0]);
					CBaseFunc::toUpperString(key);
					
					double value = 0.0;
					sscanf(atomRadii[1].c_str(), "%lf", &value);
					
					vdwRMap[key] = value;
				}
			}
		}
		
		double operator[](const string& atomtype){
			string at = CBaseFunc::eraseAll(atomtype, ' ');
			CBaseFunc::toUpperString(at);
			return vdwRMap[at];
		}
};

class Ligand {
	private:
		vector<double*> m_cared_xyz_vec;
		vector<int> m_cared_atom_orig_ind_vec;
		vector<string> m_cared_atomtype_vec;
		vector<string> m_cared_atomsimpletype_vec;
		CHEMICAL_BOND_TYPE** bt_mtx;
		
	public:
		Ligand(const string& path, const INPUT_FILE_TYPE& input_file_type, const bool& is_load_H, const bool& is_care_bond_type);
		virtual ~Ligand();
		
		const double* operator [] (const int& i);
		const int size();
		
		const vector<double*>& get_cared_xyz_vec();
		const int& get_ith_cared_atom_orig_index(const int& i);
		
		const string& get_cared_atomsimpletype_in_lig(const int& i);
		const vector<string>& get_cared_atomtype_vec_in_lig();
		
		const CHEMICAL_BOND_TYPE get_chemical_bond_type(const int& i, const int& j);
	private:
		void load_from_pdb(const string& path, const bool& is_load_H);
		void load_from_mol2(const string& path, const bool& is_load_H, const bool& is_care_bond_type);
		void load_from_sdf(const string& path, const bool& is_load_H, const bool& is_care_bond_type);
};

class ShortestRoad{
private:
	int node_num;
	int*** allRoad8Floyd;
	int** allRoadLen8Floyd;
	
	double** disMtx; 
public:
	ShortestRoad(double** adjmap, int node_num){
		this->node_num = node_num;
		
		disMtx = CBaseFunc::new2Darr(node_num, node_num);
		allRoad8Floyd = CBaseFunc::new3DIntArr(node_num, node_num, node_num, -1);
		allRoadLen8Floyd = CBaseFunc::new2DIntArr(node_num, node_num);
		
		floyd(adjmap);
	}
	
	int getNodeNum(){
		return node_num;
	}
	
	virtual ~ShortestRoad(){
		CBaseFunc::delete2Darr(disMtx, node_num);
		CBaseFunc::delete3DIntArr(node_num, node_num, allRoad8Floyd);
		if (NULL != allRoadLen8Floyd) CBaseFunc::delete2DIntArr(node_num, allRoadLen8Floyd);
	}

	int*** getAllRoad8Floyd(){
		return this->allRoad8Floyd;
	}
	
	int** getAllRoadLen8Floyd(){
		return this->allRoadLen8Floyd;
	}
	
	vector<int>* findlongestLengthRoadWithShortestDis(){
		int i = 0, j = 0;
		
		// search the longest length road with the longest shortest distance
		int maxRoadLen = 0;
		double corrRoadDis = 0;
		int* maxLenRoadInfo = NULL; // road info is "maxLenRoadInfo[0] -> ... -> maxLenRoadInfo[i] -> maxLenRoadInfo[i+1] -> ... -> maxLenRoadInfo[N]"
		for (i = 0; i < node_num; i++){
			for (j = i+1; j < node_num; j++){
				int roadLen = this->allRoadLen8Floyd[i][j];
				double dis = disMtx[i][j];
				if (roadLen > maxRoadLen){
					maxRoadLen = roadLen;
					maxLenRoadInfo = this->allRoad8Floyd[i][j];
					
					corrRoadDis = dis;
				}else if (roadLen == maxRoadLen){
					if (dis < corrRoadDis){
						maxRoadLen = roadLen;
						maxLenRoadInfo = this->allRoad8Floyd[i][j];
						
						corrRoadDis = dis;
					}
				}
			}
		}
		
		vector<int>* ans = new vector<int>();
		for (i = 0; i < node_num; i++){
			if (-1 == maxLenRoadInfo[i])
				break;
			ans->push_back(maxLenRoadInfo[i]);
		}

		return ans;
	}

private:
	/****************************************************************************
	 * @param adjmap : Symmetric Matrix, each element should be zero or positive
	 ****************************************************************************/
	void floyd(double** adjmap){
		int i = 0, j = 0, k = 0;
		double tmp;

		int** spot = CBaseFunc::new2DIntArr(node_num, node_num);
		
		for (i = 0; i < node_num; i++) {
			for (j = i; j < node_num; j++) {
				spot[i][j] = -1;
				disMtx[i][j] = adjmap[i][j];
				
				if (disMtx[i][j] <= 0)
					disMtx[i][j] = 999999999999999;
				if (i == j)
					disMtx[i][j] = 0;
					
				spot[j][i] = spot[i][j];
				disMtx[j][i] = disMtx[i][j];
			}
		}

		for (k = 0; k < node_num; k++){
			for (i = 0; i < node_num; i++){
				for (j = i; j < node_num; j++){
					tmp = disMtx[i][k] + disMtx[k][j];
					if (disMtx[i][j] > tmp) {
						disMtx[i][j] = tmp;
						spot[i][j] = k;
						
						spot[j][i] = spot[i][j];
						disMtx[j][i] = disMtx[i][j];
					}
				}
			}
		}
	
		int roadLen = 0;
		int* tmpPath = new int[node_num];
		for (i = 0; i < node_num; i++){
			for (j = i; j < node_num; j++){
				roadLen = 0;
				tmpPath[roadLen++] = i;
				recursionSearchPath8FloydAlgorithm(spot, i, j, tmpPath, roadLen);
				
				for (int k = 0; k < roadLen; k++)
					allRoad8Floyd[i][j][k] = tmpPath[k];
				allRoadLen8Floyd[i][j] = roadLen;
				
				for (int k = 0; k < roadLen; k++)
					allRoad8Floyd[j][i][k] = allRoad8Floyd[i][j][roadLen-1-k];
				allRoadLen8Floyd[j][i] = allRoadLen8Floyd[i][j];
			}
		} 
		delete[] tmpPath;
	
		CBaseFunc::delete2DIntArr(node_num, spot);
	}
	
	/****************************************************************************
	 * @param spot : the i to j throw node index, floyd algorithm spot matrix
	 * @param i : the 1th position
	 * @param j : the 2nd position
	 * @param onePath : record the shortest road from i, j
	 * @param roadLen : roadLen[0] record the road length
	 ****************************************************************************/
	 // Can be optimized, using while loop
	void recursionSearchPath8FloydAlgorithm(int** spot, int i, int j, int* path, int& roadLen) {
		if (i == j) return;
		if (spot[i][j] == -1)
			path[roadLen++] = j;
		else {
			recursionSearchPath8FloydAlgorithm(spot, i, spot[i][j], path, roadLen);
			recursionSearchPath8FloydAlgorithm(spot, spot[i][j], j, path, roadLen);
		}
	}
};

class CSort{
	public:
		// need release the return pointer
		static int* quickDescendSortIndex(const int& n, const double* arr, const int& left, const int& right){
			int* indexes = new int[n];
			for (int i = 0; i < n; i++)
				indexes[i] = i;
			
			vector<int> stack;
			stack.push_back(left);
			stack.push_back(right);
			
			while (0 != stack.size()) {
				int end = stack[stack.size()-1];
				stack.pop_back();
				int begin = stack[stack.size()-1];
				stack.pop_back();
				
				int keyi = partition_of_quickDescendSortIndex(arr, indexes, begin, end);
				
				if (keyi+1 < end) {
					stack.push_back(keyi+1);
					stack.push_back(end);
				}
				if (begin < keyi-1) {
					stack.push_back(begin);
					stack.push_back(keyi-1);
				}
			}
			
			return indexes;
		}
		
		// need release the return pointer
		static int* quickAscendSortIndex(const int& n, const double* arr, const int& left, const int& right){
			int* indexes = new int[n];
			for (int i = 0; i < n; i++)
				indexes[i] = i;
			
			vector<int> stack;
			stack.push_back(left);
			stack.push_back(right);
			
			while (0 != stack.size()) {
				int end = stack[stack.size()-1];
				stack.pop_back();
				int begin = stack[stack.size()-1];
				stack.pop_back();
				
				int keyi = partition_of_quickAscendSortIndex(arr, indexes, begin, end);
				
				if (keyi+1 < end) {
					stack.push_back(keyi+1);
					stack.push_back(end);
				}
				if (begin < keyi-1) {
					stack.push_back(begin);
					stack.push_back(keyi-1);
				}
			}
			
			return indexes;
		}
		
		// need release the return pointer
		static int* quickAscendSortIndex(const int& n, const int* arr, const int& left, const int& right){
			int* indexes = new int[n];
			for (int i = 0; i < n; i++)
				indexes[i] = i;
			
			vector<int> stack;
			stack.push_back(left);
			stack.push_back(right);
			
			while (0 != stack.size()) {
				int end = stack[stack.size()-1];
				stack.pop_back();
				int begin = stack[stack.size()-1];
				stack.pop_back();
				
				int keyi = partition_of_quickAscendSortIndex(arr, indexes, begin, end);
				
				if (keyi+1 < end) {
					stack.push_back(keyi+1);
					stack.push_back(end);
				}
				if (begin < keyi-1) {
					stack.push_back(begin);
					stack.push_back(keyi-1);
				}
			}
			
			return indexes;
		}
		
		static int find_max_index(const int& n, const double* arr){
			int max_ind = 0;
			for (int i = 1; i < n; i++){
				if (arr[i] > arr[max_ind]){
					max_ind = i;
				}
			}
			
			return max_ind;
		}
	
	private:
		static int partition_of_quickDescendSortIndex(const double* arr, int* indexes, const int& __left, const int& __right) {
			int left = __left;
			int right = __right;
			int pivot = indexes[left];
	        while (left < right) {
	            while (left < right && arr[indexes[right]] < arr[pivot]) {  
	                right--;  
	            }  
	            indexes[left] = indexes[right];  
	            while (left < right && arr[indexes[left]] >= arr[pivot]) {  
	                left++; 
	            }  
	            indexes[right] = indexes[left];  
	        }
	        
	        indexes[left] = pivot;  
	        return left;  
		}
		
		static int partition_of_quickAscendSortIndex(const double* arr, int* indexes, const int& __left, const int& __right) {
			int left = __left;
			int right = __right;
			int pivot = indexes[left];
	        while (left < right) {
	            while (left < right && arr[indexes[right]] > arr[pivot]) {  
	                right--;  
	            }  
	            indexes[left] = indexes[right];
	            while (left < right && arr[indexes[left]] <= arr[pivot]) {
	                left++; 
	            }  
	            indexes[right] = indexes[left];  
	        }
	        
	        indexes[left] = pivot;  
	        return left;  
		}
		
		static int partition_of_quickAscendSortIndex(const int* arr, int* indexes, const int& __left, const int& __right) {
			int left = __left;
			int right = __right;
			int pivot = indexes[left];
	        while (left < right) {
	            while (left < right && arr[indexes[right]] > arr[pivot]) {  
	                right--;  
	            }  
	            indexes[left] = indexes[right];
	            while (left < right && arr[indexes[left]] <= arr[pivot]) {
	                left++; 
	            }  
	            indexes[right] = indexes[left];  
	        }
	        
	        indexes[left] = pivot;  
	        return left;  
		}
};

class LigAtomMatcher {
	private:
		int atnum;
		Ligand& lig;
		ShortestRoad *sr;
		
		bool** is_simple_same_imp_mtx;  // jugde identitcal atoms without shortest road
		bool** is_same_imp_mtx;  // jugde identitcal atoms with shortest road
		
		vector<vector<int>* > atgs; // atom groups
		bool** togethor_mappings; // judge wheter the ith atom group can mapping alone
		
		vector<vector<SIMPLE_ROAD* >* > attypes_in_roads;
		
		// ats[i]: atom type of ith atom in lig
		vector<string> ats;
		
		// cbtss[i]: bond types of neigbors of ith atom in lig
		vector<vector<CHEMICAL_BOND_TYPE> > cbtss;
		
		// natss[i]: atom types of neigbors of ith atom in lig
		vector<vector<string> > natss;
	public:
		LigAtomMatcher(Ligand* p_lig);
		virtual ~LigAtomMatcher();
		const int& size();
		const bool& is_same_important(const int& i, const int& j);
		
		const string& get_ith_at(const int& i);
		const vector<CHEMICAL_BOND_TYPE>& get_ith_cbts(const int& i);
		const vector<string>& get_ith_nats(const int& i);
		const vector<SIMPLE_ROAD* >& get_ith_simple_roads(const int& i);
		const SIMPLE_ROAD* get_ij_simple_road(const int& i, const int& j);
		
		Ligand& get_lig(){
			return lig;
		}
		
		const bool& is_ij_atgs_togethor_mapping(int i, int j){
			generate_backtrace_mapping_relation_mtx();
			return togethor_mappings[i][j];
		}
				
		static vector<vector<ALIGN_NODE> >* generate_potentail_align_nodes(LigAtomMatcher& querym, LigAtomMatcher& templm, int* out_part_q2t);
	private:
		bool is_same_roads(const vector<SIMPLE_ROAD* >& arvec, const vector<SIMPLE_ROAD* >& brvec);
		vector<SIMPLE_ROAD* >* extract_ith_roads(int** ar, int* arl);
		void extract_atgs();
		
		void generate_backtrace_mapping_relation_mtx(){
			if (NULL != this->togethor_mappings) return;
			int atgs_size = atgs.size();
			
			int one_atom_atg_num = 0;
			bool* is_one_atom_arr = new bool[atgs_size];
			for (int i = 0; i < atgs_size; i++){
				if (1 == atgs[i]->size()){
					is_one_atom_arr[i] = true;
					one_atom_atg_num++;
				} else is_one_atom_arr[i] = false;
			}
			
			if (one_atom_atg_num >= 2){
				togethor_mappings = CBaseFunc::new2DBoolArr(atgs_size, atgs_size);
				
				int*** all_roads = sr->getAllRoad8Floyd();
				int** all_road_lens = sr->getAllRoadLen8Floyd();
				
				int* atind_2_atgind = new int[atnum];
				for (int i = 0; i < atgs_size; i++){
					vector<int> ith_atgs = *atgs[i];
					int isize = ith_atgs.size();
					
					for (int j = 0; j < isize; j++)
						atind_2_atgind[ith_atgs[j]] = i;
				}
				
				for (int i = 0; i < atgs_size; i++){
					togethor_mappings[i][i] = true;
					if (!is_one_atom_arr[i]){
						vector<int> ith_atg = *atgs[i];
						int isize = ith_atg.size();
						
						for (int j = i+1; j < atgs_size; j++){
							if (!is_one_atom_arr[j]){
								vector<int> jth_atg = *atgs[j];
								int jsize = jth_atg.size();
								
								bool is_together = false;
								for (int k = 0; k < isize; k++){
									int kind = ith_atg[k];
									for (int l = 0; l < jsize; l++){
										int lind = jth_atg[l];
										int kl_road_len = all_road_lens[kind][lind];
										int* kl_road = all_roads[kind][lind];
										
										int num_of_one_atom_mapping = 0;
										for (int m = 0; m < kl_road_len; m++){
											int mind = kl_road[m];
											if (is_one_atom_arr[atind_2_atgind[mind]]){
												num_of_one_atom_mapping++;
												if (num_of_one_atom_mapping >= 2)
													break;
											}
										}
										
										if (num_of_one_atom_mapping < 2){
											is_together = true;
											break;
										}
									}
									
									if (is_together) break;
								}
								
								togethor_mappings[i][j] = togethor_mappings[j][i] = is_together;		
							}
						}
					}
				}
				
				delete[] atind_2_atgind;
			}else{
				togethor_mappings = CBaseFunc::new2DBoolArr(atgs_size, atgs_size, true);
			}
			
			delete[] is_one_atom_arr;
		}
		
		bool is_simple_same_important(const int& i, const int& j);
	public:
		static bool is_same_important(LigAtomMatcher& ilam, int& i, LigAtomMatcher& jlam, int& j, bool** is_simple_important_mtx_between_ilam_and_jlam);
		static bool is_simple_same_important(LigAtomMatcher& ilam, int& i, LigAtomMatcher& jlam, int& j);
		static bool is_same_road(LigAtomMatcher& qlam, int& qi, int& qj, LigAtomMatcher& tlam, int& ti, int& tj, bool** is_same_important_mtx_between_ilam_and_jlam);
};

class Backtracking8LSscore {
	private:
		vector<ALIGN_NODE>& nodes;
		LigAtomMatcher& qlam;
		LigAtomMatcher& tlam;
		Ligand* query; // [donot need release]
		Ligand* templ; // [donot need release]
		double d02;
		
		int qsize;
		int match_num;
		double highest_LSscore;
		int node_num;

		// for Bron-Kerbosch algorithm
		clock_t start_t;
		bool** edges; // graph map [need release]
		int** some;  // P set [need release]
		int** none;  // X set [need release]
		int** all;   // R set [need release]
		int* best; // [need release]
		double* node_LSsco_items; // [need release]
		
		// for output
		int* q2t; // [need release]
		double* q2t_dis2; // [need release]
	public:
		Backtracking8LSscore(vector<ALIGN_NODE>& nodes, LigAtomMatcher& qlam, LigAtomMatcher& tlam, double& d02, int& match_num) : 
				nodes(nodes), qlam(qlam), tlam(tlam), d02(d02), match_num(match_num){
			int i, j, k;
			
			this->query = &qlam.get_lig();
			this->templ = &tlam.get_lig();
			this->qsize = query->size();
			this->highest_LSscore = 0.;
			this->node_num = nodes.size();
			this->q2t = new int[qsize];
			this->q2t_dis2 = new double[qsize];
						
			{
				// init state matrix for bron_kerbosch algorthm	
				this->edges = CBaseFunc::new2DBoolArr(node_num+1, node_num+1);
				for (i = 0; i < node_num; i++){
					ALIGN_NODE& inode = this->nodes[i];
					for (j = i+1; j < node_num; j++){
						ALIGN_NODE& jnode = this->nodes[j];
						const SIMPLE_ROAD* qroad = qlam.get_ij_simple_road(inode.qind, jnode.qind);
						const SIMPLE_ROAD* troad = tlam.get_ij_simple_road(inode.tind, jnode.tind);
						
						edges[i+1][j+1] = edges[j+1][i+1]
							= (inode.qind != jnode.qind && inode.tind != jnode.tind && qroad->roadlen == troad->roadlen);
					}
				}
				
				this->some = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->none = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->all = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->best = CBaseFunc::new1DIntArr(match_num, -1);
				
				node_LSsco_items = new double[node_num];
				for (i = 0; i < node_num; i++)
					node_LSsco_items[i] = 1. / (1. + nodes[i].dis2/d02);
				int* sinds = CSort::quickDescendSortIndex(node_num, node_LSsco_items, 0, node_num-1);
				for (i = 0; i < node_num; i++)
					some[1][i] = sinds[i]+1;
				
				start_t = clock();	
				bron_kerbosch(1, 0., 0, node_num, 0);
				
				delete[] sinds; 
			}
			
			this->parse_atommapping();
		}
		
		virtual ~Backtracking8LSscore(){
			delete[] q2t_dis2;
			delete[] q2t;
			delete[] best;
			delete[] node_LSsco_items;
			CBaseFunc::delete2DIntArr(node_num+2, all);
			CBaseFunc::delete2DIntArr(node_num+2, none);
			CBaseFunc::delete2DIntArr(node_num+2, some);
			CBaseFunc::delete2DBoolArr(node_num+1, edges);
		}
		
		double get_highest_LSscore(){
			return this->highest_LSscore; 
		}
		
		int operator [](const int& i){
			return this->q2t[i];
		}
		
		double get_ith_atommapping_dis2(const int& i){
			return this->q2t_dis2[i];
		}
		
	private:
		// Time Complexity: O(3^(n/3)), comes from: 
		//   1. https://www.jianshu.com/p/437bd6936dad
		//   2. https://dl.acm.org/doi/pdf/10.1145/362342.362367
		// Please don't casually change others' code, thank you.
		void bron_kerbosch(	int d /*depth*/,
							double LSscore /*LS-score*/,
		                	int an /*index for all (R)*/,
							int sn /*index for some (P)*/,
							int nn /*index for none (X)*/){
			// we know the maxclique size of this graph is 'match_num'
			if (0 == sn && 0 == nn){
				if (an == this->match_num){
					// Report R as a maximal clique
					if (LSscore > this->highest_LSscore){
						this->highest_LSscore = LSscore;
						for (int i = 0; i < this->match_num; i++)
							best[i] = all[d][i];
					}
				}
			}
			
			clock_t end_t = clock();
			double use_seconds = 1.0*(end_t - start_t)/CLOCKS_PER_SEC;
			if (use_seconds > g_seconds)
				return;
			
			// we know the maxclique size of this graph is 'match_num'
			if (0 != sn && an < match_num && an+sn >= match_num) {
				for (int j = 0; j < an; j++)
					all[d+1][j] = all[d][j];
				
				int u = some[d][0];
				for (int i = 0; i < sn; i++){
					int v = some[d][i];
					if (edges[u][v])
						continue;
					
					all[d+1][an] = v;
					double current_LSscore = LSscore + this->node_LSsco_items[all[d+1][an]-1];
					
					int tsn = 0, tnn = 0;
					for (int j = 0; j < sn; j++)
						if (edges[v][some[d][j]])
							some[d+1][tsn++] = some[d][j];
							
					double next_LSscore = 0.;
					int miss_num = match_num - (an+1);
					for (int j = 0; j < tsn && j < miss_num; j++)
						if (edges[v][some[d+1][j]])
							next_LSscore += this->node_LSsco_items[some[d+1][j]-1];
					
					if (current_LSscore+next_LSscore > highest_LSscore){
						for (int j = 0; j < nn; j++)
							if (edges[v][none[d][j]])
								none[d+1][tnn++] = none[d][j];
							
						bron_kerbosch(d+1, current_LSscore, an+1, tsn, tnn);
					}
					
					some[d][i] = 0;
					none[d][nn++] = v;
				}
			}
		}
		
		void parse_atommapping(){
			int i = 0;
			for (; i < qsize; i++)
				q2t[i] = -1;
			for (i = 0; i < match_num; i++){
				if (-1 == best[i]){
					cout << "Error: Two 3D structure files donot come from the same ligand." << endl;
					cout << "       Please check and re-run it by DockEva." << endl;
					exit(-1);
				}
				ALIGN_NODE node = nodes[best[i]-1];
				q2t[node.qind] = node.tind;
				q2t_dis2[node.qind] = node.dis2;
			}
		}
};

class Backtracking8RMSD {
	private:
		vector<ALIGN_NODE>& nodes;
		LigAtomMatcher& qlam;
		LigAtomMatcher& tlam;
		Ligand* query; // [donot need release]
		Ligand* templ; // [donot need release]
		
		int qsize;
		int match_num;
		double lowest_RMSD2;
		int node_num;

		// for Bron-Kerbosch algorithm
		clock_t start_t;
		bool** edges; // graph map [need release]
		int** some;  // P set [need release]
		int** none;  // X set [need release]
		int** all;   // R set [need release]
		int* best; // [need release]
		
		// for output
		int* q2t; // [need release]
		double* q2t_dis2; // [need release]
	public:
		Backtracking8RMSD(vector<ALIGN_NODE>& nodes, LigAtomMatcher& qlam, LigAtomMatcher& tlam, int& match_num) : 
				nodes(nodes), qlam(qlam), tlam(tlam), match_num(match_num) {
			int i, j, k;
			
			this->query = &qlam.get_lig();
			this->templ = &tlam.get_lig();
			this->qsize = query->size();
			this->lowest_RMSD2 = g_inf;
			this->node_num = nodes.size();
			this->q2t = new int[qsize];
			this->q2t_dis2 = new double[qsize];
			
			{
				// init state matrix for bron_kerbosch algorthm	
				this->edges = CBaseFunc::new2DBoolArr(node_num+1, node_num+1);
				for (i = 0; i < node_num; i++){
					ALIGN_NODE& inode = this->nodes[i];
					for (j = i+1; j < node_num; j++){
						ALIGN_NODE& jnode = this->nodes[j];
						const SIMPLE_ROAD* qroad = qlam.get_ij_simple_road(inode.qind, jnode.qind);
						const SIMPLE_ROAD* troad = tlam.get_ij_simple_road(inode.tind, jnode.tind);
						
						edges[i+1][j+1] = edges[j+1][i+1]
							= (inode.qind != jnode.qind && inode.tind != jnode.tind && qroad->roadlen == troad->roadlen);
					}
				}
				
				this->some = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->none = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->all = CBaseFunc::new2DIntArr(node_num+2, node_num+2, 0);
				this->best = CBaseFunc::new1DIntArr(match_num, -1);
				
				double* dis2s = new double[node_num];
				for (i = 0; i < node_num; i++)
					dis2s[i] = nodes[i].dis2;
				int* sinds = CSort::quickAscendSortIndex(node_num, dis2s, 0, node_num-1);
				for (i = 0; i < node_num; i++)
					some[1][i] = sinds[i]+1;
				
				start_t = clock();
				bron_kerbosch(1, 0., 0, node_num, 0);
				
				delete[] dis2s;
				delete[] sinds; 
			}
			
			this->parse_atommapping();
		}
		
		virtual ~Backtracking8RMSD(){
			delete[] q2t_dis2;
			delete[] q2t;
			delete[] best;
			CBaseFunc::delete2DIntArr(node_num+2, all);
			CBaseFunc::delete2DIntArr(node_num+2, none);
			CBaseFunc::delete2DIntArr(node_num+2, some);
			CBaseFunc::delete2DBoolArr(node_num+1, edges);
		}
		
		double get_lowest_RMSD2(){
			return lowest_RMSD2; 
		}
		
		int operator [](const int& i){
			return this->q2t[i];
		}
		
		double get_ith_atommapping_dis2(const int& i){
			return this->q2t_dis2[i];
		}
		
	private:
		// Time Complexity: O(3^(n/3)), comes from: 
		//   1. https://www.jianshu.com/p/437bd6936dad
		//   2. https://dl.acm.org/doi/pdf/10.1145/362342.362367
		// Please don't casually change others' code, thank you.
		void bron_kerbosch(	int d /*depth*/,
							double rmsd2 /*rmsd on previous depth*/, 
		                	int an /*index for all (R)*/,
							int sn /*index for some (P)*/,
							int nn /*index for none (X)*/){
			// we know the maxclique size of this graph is 'match_num'
			if (0 == sn && 0 == nn){
				if (an == this->match_num){
					// Report R as a maximal clique
					if (rmsd2 < this->lowest_RMSD2){
						this->lowest_RMSD2 = rmsd2;
						for (int i = 0; i < this->match_num; i++)
							best[i] = all[d][i];
					}
				}
			}
			
			clock_t end_t = clock();
			double use_seconds = 1.0*(end_t - start_t)/CLOCKS_PER_SEC;
			if (use_seconds > g_seconds)
				return;
			
			// we know the maxclique size of this graph is 'match_num'
			if (0 != sn && an < match_num && an+sn >= match_num) {
				for (int j = 0; j < an; j++)
					all[d+1][j] = all[d][j];
				
				int u = some[d][0];
				for (int i = 0; i < sn; i++){
					int v = some[d][i];
					if (edges[u][v])
						continue;
					
					all[d+1][an] = v;
					double current_rmsd2 = rmsd2 + this->nodes[all[d+1][an]-1].dis2;
					if (current_rmsd2 > this->lowest_RMSD2)
						continue;
					
					int tsn = 0, tnn = 0;
					for (int j = 0; j < sn; j++)
						if (edges[v][some[d][j]])
							some[d+1][tsn++] = some[d][j];
					
					bool is_need_go_depth = true;
					double next_best_rmsd2 = current_rmsd2;
					int miss_num = match_num - (an+1);
					for (int j = 0; j < tsn && j < miss_num; j++){
						if (edges[v][some[d+1][j]]){
							next_best_rmsd2 += this->nodes[some[d+1][j]-1].dis2;
							if (next_best_rmsd2 > this->lowest_RMSD2){
								is_need_go_depth = false;
								break;
							}
						}
					}
					
					if (is_need_go_depth){
						for (int j = 0; j < nn; j++)
							if (edges[v][none[d][j]])
								none[d+1][tnn++] = none[d][j];
							
						bron_kerbosch(d+1, current_rmsd2, an+1, tsn, tnn);
					}
					
					some[d][i] = 0;
					none[d][nn++] = v;
				}
			}
		}
		
		void parse_atommapping(){
			int i = 0;
			for (; i < qsize; i++)
				q2t[i] = -1;
			for (i = 0; i < match_num; i++){
				if (-1 == best[i]){
					cout << "Error: Two 3D structure files donot come from the same ligand." << endl;
					cout << "       Please check and re-run it by DockEva." << endl;
					exit(-1);
				}
				ALIGN_NODE node = nodes[best[i]-1];
				q2t[node.qind] = node.tind;
				q2t_dis2[node.qind] = node.dis2;
			}
		}
};

class CDockEvaluator {
	private:
		Ligand* query;
		Ligand* templ;
		
		double lsscore;
		double rmsd;
		double d0;
		
		vector<ALIGN_PAIR> aa_level_ali;
	public:
		CDockEvaluator(const string& qfile, const string& tfile, const INPUT_FILE_TYPE& input_file_type, const bool& lsscore_or_rmsd, const bool& is_load_H, const bool& is_care_bond_type);
		virtual ~CDockEvaluator();
		
		const double& get_use_seconds();
		const double& get_lsscore();
		const double& get_rmsd();
		
		void print_result();
	private:
		void align_monomer(const bool& lsscore_or_rmsd);
};

int main(int argc, char** args) {
	CBaseFunc::print_logo();
	
	TOOL_EXE = args[0];
	
	int i, j, fileInd = 0;
	
	string query_file;
	string templ_file;
	bool isQueryProvide = false;
	bool isTemplProvide = false;
	INPUT_FILE_TYPE input_file_type = MOL2;
	bool lsscore_or_rmsd = false;
	bool is_load_H = false;
	bool is_care_bond_type = true; 
  	
  	//--------------------------------------------------------------------------//
	//----------------          Load Input Parameters      ---------------------//
	//--------------------------------------------------------------------------//
	for (i = 1; i < argc; i++){
		if (0 == strcmp(args[i], "-t") && i < argc-1){
			if (0 == strcmp(args[i+1], "pdb"))
				input_file_type = PDB;
			else if (0 == strcmp(args[i+1], "sdf"))
				input_file_type = SDF;
			else
				input_file_type = MOL2;
		}else if (0 == strcmp(args[i], "-s") && i < argc-1){
			if (0 == strcmp(args[i+1], "lssco"))
				lsscore_or_rmsd = true;
		}else if (0 == strcmp(args[i], "-cbt") && i < argc-1){
			if (0 == strcmp(args[i+1], "N") || 0 == strcmp(args[i+1], "n"))
				is_care_bond_type = false;
		}else if (0 == strcmp(args[i], "-maxrt") && i < argc-1){
			double tmp = atof(args[++i]);
			if (0 < tmp) g_seconds = tmp*60;
		}else if (0 == strcmp(args[i], "-lh") && i < argc-1){
			if (0 == strcmp(args[i+1], "Y") || 0 == strcmp(args[i+1], "y"))
				is_load_H = true;
		}else if (0 == strcmp(args[i], "-h")){
			CBaseFunc::print_help(args[0]);
		}else if (0 == strcmp(args[i], "-v")){
			exit(1);
		}else{
			if (fileInd == 0){
				isQueryProvide = true;
				query_file = args[i];
			}else if (fileInd == 1){
				isTemplProvide = true;
				templ_file = args[i];
			}
			fileInd++;
		}
	}
	
	if (!isQueryProvide){
		cout << "PLEASE PROVIDE lig1.mol2/lig1.sdf/lig1.pdb FILE!!!" << endl << endl;
		CBaseFunc::print_help(args[0]);
	}else{
		fstream _file;
		_file.open(query_file.c_str(), ios::in);
		if(!_file){
			cout << query_file << " is not existed!" << endl;
			cout << "Please check it and input a correct PDB file path!" << endl;
			exit(1);
		}
	}
	
	if (!isTemplProvide){
		cout << "PLEASE PROVIDE lig2.mol2/lig2.sdf/lig2.pdb FILE!!!" << endl << endl;
		CBaseFunc::print_help(args[0]);
	}else{
		fstream _file;
		_file.open(templ_file.c_str(), ios::in);
		if(!_file){
			cout << templ_file << " is not existed!" << endl;
			cout << "Please check it and input a correct PDB file path!" << endl;
			exit(1);
		}
	}
	
	clock_t start_t, end_t;
	start_t = clock();
	
	CDockEvaluator* mtm = new CDockEvaluator(query_file, templ_file, input_file_type, lsscore_or_rmsd, is_load_H, is_care_bond_type);
	
	end_t = clock();
	double use_seconds = 1.0*(end_t - start_t)/CLOCKS_PER_SEC;
	
	mtm->print_result();
	cout << "Taking " << setprecision(8) << use_seconds << " seconds in total." << endl;
	
	delete mtm;
	return 0;
}

//int main(){
//	CBaseFunc::print_logo();
//	
//	clock_t start_t, end_t;
//	start_t = clock();
//
//	string qf = "D:/buf/3cyu/vina1.mol2";
//	string tf = "D:/buf/3cyu/vina3.mol2";
//
////	string qf = "D:/buf/8fy1/crystal.mol2";  
////	string tf = "D:/buf/8fy1/vina1.mol2";
//	
//	CDockEvaluator* mtm = new CDockEvaluator(qf, tf, MOL2, false, false, true);
//	mtm->print_result();
//	delete mtm;
//
//	end_t = clock();
//	double use_seconds = 1.0*(end_t - start_t)/CLOCKS_PER_SEC;
//	cout << "Taking " << setprecision(8) << use_seconds << " seconds in total." << endl;
//	
//	return 0;
//}

inline vector<vector<ALIGN_NODE> >* LigAtomMatcher::generate_potentail_align_nodes(LigAtomMatcher& querym, LigAtomMatcher& templm, int* out_part_q2t){
	int i = 0;
	int j = 0;
	int k = 0;
	int l = 0;
	
	LigAtomMatcher& qobj = querym;
	LigAtomMatcher& tobj = templm;
	Ligand& query = querym.lig;
	Ligand& templ = templm.lig;
	
	vector<vector<int>* >& qatgs = qobj.atgs;
	vector<vector<int>* >& tatgs = tobj.atgs;
	
	int mx = qatgs.size();
	int nx = tatgs.size();
	
	int m = query.size();
	int n = templ.size();
	
	bool** is_simple_important_mtx_between_ilam_and_jlam = CBaseFunc::new2DBoolArr(m, n);
	for (i = 0; i < m; i++){
		for (j = 0; j < n; j++){
			is_simple_important_mtx_between_ilam_and_jlam[i][j] = is_simple_same_important(qobj, i, tobj, j); 
		}
	}
	
	vector<vector<ALIGN_NODE>* > __align_nodes;
	bool* is_used = CBaseFunc::new1Dbool(nx);
	for (i = 0; i < mx; i++){
		vector<int>& ith = *qatgs[i];
		int mm = ith.size();
		int matched_j = -1;
		for (j = 0; j < nx; j++){
			if (is_used[j]) continue;
			vector<int>& jth = *tatgs[j];
			if (is_same_important(qobj, ith[0], tobj, jth[0], is_simple_important_mtx_between_ilam_and_jlam)){
				int nn = jth.size();
				
				if (mm == 1){
					out_part_q2t[ith[0]] = jth[0];
					__align_nodes.push_back(NULL);
				}else{
					vector<ALIGN_NODE>* potentail_align_nodes = new vector<ALIGN_NODE>();
					for (k = 0; k < mm; k++){
						for (l = 0; l < nn; l++){
							double dis2 = CBaseFunc::distance2(query[ith[k]], templ[jth[l]]);
							
							ALIGN_NODE node;
							node.qind = ith[k];
							node.tind = jth[l];
							node.dis2 = dis2; 
							potentail_align_nodes->push_back(node);
						}
					}
					__align_nodes.push_back(potentail_align_nodes);		
				}
				
				is_used[j] = true;
				matched_j = j;
				break;
			}
		}
		if (matched_j == -1){
			cout << "* ERROR : there are two ligands with same name but different structure topologies." << endl;
			exit(-1);
		}
	}
	
	vector<vector<ALIGN_NODE> >* ans = new vector<vector<ALIGN_NODE> >();
	for (i = 0; i < mx; i++)
		is_used[i] = false;
	for (i = 0; i < mx; i++){
		vector<ALIGN_NODE> ith;
		for (j = 0; j < mx; j++){
			if (is_used[j]) continue;
			if (querym.is_ij_atgs_togethor_mapping(i, j)){
				vector<ALIGN_NODE>* jitem = __align_nodes[j];
				if (NULL == jitem) continue;
				
				int jsize = jitem->size();
				for (k = 0; k < jsize; k++)
					ith.push_back((*jitem)[k]);
				
				is_used[j] = true;
			}
		}
		
		if (ith.size() != 0) ans->push_back(ith);
	}
	
	for (i = 0; i < mx; i++)
		if (NULL != __align_nodes[i])
			delete __align_nodes[i];
	CBaseFunc::delete2DBoolArr(m, is_simple_important_mtx_between_ilam_and_jlam);
	delete[] is_used;
	
	return ans;
}

inline const int& LigAtomMatcher::size(){
	return atnum;
}

inline void CDockEvaluator::align_monomer(const bool& lsscore_or_rmsd){
	int i, j, iali;
	
	Ligand* qmol = this->query;
	Ligand* tmol = this->templ;
	int qmol_len = qmol->size();
	int tmol_len = tmol->size();
	
	if (tmol_len != qmol_len){
		cout << "* Error: the ligand atom numbers are not same." << endl;
		exit(-1);
	}
	
	vector<string> aseq_vec = qmol->get_cared_atomtype_vec_in_lig();
	vector<string> bseq_vec = tmol->get_cared_atomtype_vec_in_lig();
	
	d0 = CBaseFunc::d0_of_lsscore(qmol_len);
	double d02 = d0*d0;
	
	LigAtomMatcher qmatcher(qmol);
	LigAtomMatcher tmatcher(tmol);
	
	int* q2t_on_one_atom_groups = CBaseFunc::new1DIntArr(qmol_len, -1);
	vector<vector<ALIGN_NODE> >* p_potentail_align_nodes_arr = LigAtomMatcher::generate_potentail_align_nodes(qmatcher, tmatcher, q2t_on_one_atom_groups);
	if (lsscore_or_rmsd){
		rmsd = 0.;
		lsscore = 0.;
		int ali_count = 0;
		
		int __size =  p_potentail_align_nodes_arr->size();
		for (i = 0; i < __size; i++) {
			vector<ALIGN_NODE> potentail_align_nodes = (*p_potentail_align_nodes_arr)[i];
			int multi_match_num = 0, node_num = potentail_align_nodes.size();
			bool* is_used = CBaseFunc::new1Dbool(qmol_len);
			for (j = 0; j < node_num; j++) {
				int qind = potentail_align_nodes[j].qind;
				if (is_used[qind]) continue;
				
				multi_match_num++;
				is_used[qind] = true;
			}
			delete[] is_used;
			
			Backtracking8LSscore bcktrace(potentail_align_nodes, qmatcher, tmatcher, d02, multi_match_num);
			
			lsscore += bcktrace.get_highest_LSscore();
			for (j = 0; j < qmol_len; j++){
				if (-1 != bcktrace[j]){
					ALIGN_PAIR ap;
					ap.qind = j;
					ap.tind = bcktrace[j];
					ap.qoind = qmol->get_ith_cared_atom_orig_index(j);
					ap.toind = tmol->get_ith_cared_atom_orig_index(bcktrace[j]);
					ap.qaa = aseq_vec[j];
					ap.taa = bseq_vec[bcktrace[j]];
					ap.dis2 = bcktrace.get_ith_atommapping_dis2(j);
					aa_level_ali.push_back(ap);
					
					rmsd += ap.dis2;
					ali_count++;
				}
			}
		}
		
		for (i = 0; i < qmol_len; i++){
			if (-1 != q2t_on_one_atom_groups[i]){
				ALIGN_PAIR ap;
				ap.qind = i;
				ap.tind = q2t_on_one_atom_groups[i];
				ap.qoind = qmol->get_ith_cared_atom_orig_index(i);
				ap.toind = tmol->get_ith_cared_atom_orig_index(q2t_on_one_atom_groups[i]);
				ap.qaa = aseq_vec[i];
				ap.taa = bseq_vec[q2t_on_one_atom_groups[i]];
				ap.dis2 = CBaseFunc::distance2(qmol->get_cared_xyz_vec()[i], tmol->get_cared_xyz_vec()[q2t_on_one_atom_groups[i]]);
				aa_level_ali.push_back(ap);
				
				lsscore += 1./(1. + ap.dis2/d02);
				rmsd += ap.dis2;
				ali_count++;
			}
		}
		
		lsscore /= qmol_len;
		rmsd = sqrt(rmsd/qmol_len);
		if (ali_count != qmol_len){
			cout << "ERROR: the ligand atoms or their topology information are not same." << endl;
			exit(-1);
		}
	} else {
		rmsd = 0.;
		lsscore = 0.;
		int ali_count = 0;
		
		int __size =  p_potentail_align_nodes_arr->size();
		for (i = 0; i < __size; i++) {
			vector<ALIGN_NODE> potentail_align_nodes = (*p_potentail_align_nodes_arr)[i];
			int multi_match_num = 0, node_num = potentail_align_nodes.size();
			bool* is_used = CBaseFunc::new1Dbool(qmol_len);
			for (j = 0; j < node_num; j++) {
				int qind = potentail_align_nodes[j].qind;
				if (is_used[qind]) continue;
				
				multi_match_num++;
				is_used[qind] = true;
			}
			delete[] is_used;
			
			Backtracking8RMSD bcktrace(potentail_align_nodes, qmatcher, tmatcher, multi_match_num);
			
			rmsd += bcktrace.get_lowest_RMSD2();
			for (j = 0; j < qmol_len; j++){
				if (-1 != bcktrace[j]){
					ALIGN_PAIR ap;
					ap.qind = j;
					ap.tind = bcktrace[j];
					ap.qoind = qmol->get_ith_cared_atom_orig_index(j);
					ap.toind = tmol->get_ith_cared_atom_orig_index(bcktrace[j]);
					ap.qaa = aseq_vec[j];
					ap.taa = bseq_vec[bcktrace[j]];
					ap.dis2 = bcktrace.get_ith_atommapping_dis2(j);
					aa_level_ali.push_back(ap);
					
					lsscore += 1./(1. + ap.dis2/d02);
					ali_count++;
				}
			}
		}
		
		for (i = 0; i < qmol_len; i++){
			if (-1 != q2t_on_one_atom_groups[i]){
				ALIGN_PAIR ap;
				ap.qind = i;
				ap.tind = q2t_on_one_atom_groups[i];
				ap.qoind = qmol->get_ith_cared_atom_orig_index(i);
				ap.toind = tmol->get_ith_cared_atom_orig_index(q2t_on_one_atom_groups[i]);
				ap.qaa = aseq_vec[i];
				ap.taa = bseq_vec[q2t_on_one_atom_groups[i]];
				ap.dis2 = CBaseFunc::distance2(qmol->get_cared_xyz_vec()[i], tmol->get_cared_xyz_vec()[q2t_on_one_atom_groups[i]]);
				aa_level_ali.push_back(ap);
				
				lsscore += 1./(1. + ap.dis2/d02);
				rmsd += ap.dis2;
				ali_count++;
			}
		}
		
		lsscore /= qmol_len;
		rmsd = sqrt(rmsd/qmol_len);
		if (ali_count != qmol_len){
			cout << "ERROR: the ligand atoms or their topology information are not same." << endl;
			exit(-1);
		}
	}
	
	delete p_potentail_align_nodes_arr;
}

inline CDockEvaluator::CDockEvaluator(const string& qfile, const string& tfile, const INPUT_FILE_TYPE& input_file_type, const bool& lsscore_or_rmsd, const bool& is_load_H, const bool& is_care_bond_type){
	int i, j, k, n;
	
	this->query = new Ligand(qfile, input_file_type, is_load_H, is_care_bond_type);
	this->templ = new Ligand(tfile, input_file_type, is_load_H, is_care_bond_type);
	
	align_monomer(lsscore_or_rmsd);
}

inline CDockEvaluator::~CDockEvaluator(){
	delete query;
	delete templ;
	vector<ALIGN_PAIR>().swap(this->aa_level_ali);
}

inline string CBaseFunc::charVec2String(const vector<char>& vec){
	int size = vec.size();
	char* parr = new char[size+1];
	for (int i = 0; i < size; i++)
		parr[i] = vec[i];
	parr[size] = '\0';
	
	string ans(parr);
	delete[] parr; parr = NULL;
	return ans;
}

inline CBaseFunc::CBaseFunc()
{

}

inline CBaseFunc::~CBaseFunc()
{

}


/*******************************************************
 * @param r : the row number of the 2D matrix
 * @param c : the column number of the 2D matrix
 * @return  : the pointer of the new 2D matrix
 *******************************************************/
inline double** CBaseFunc::new2Darr(const int& r, const int& c){
	double** ans = new double*[r];
	for (int i = 0; i < r; i++){
		ans[i] = new double[c];
		for (int j = 0; j < c; j++){
			ans[i][j] = 0.0;
		}
	}

	return ans;
}

/*******************************************************
 * @param r : the row number of the 2D matrix
 * @function: release the memory of the 2D matrix
 *******************************************************/
inline void CBaseFunc::delete2Darr(double** pMtx, const int& r){
	for (int i = 0; i < r; i++){
		delete[] pMtx[i];
	}
	delete[] pMtx;
	pMtx = NULL;
}

inline int** CBaseFunc::new2DIntArr(const int& row, const int& col){
	int **ans=new int*[row];
	for(int i=0;i<row;i++){
		ans[i]=new int[col];
		for(int j=0; j<col; j++)
			ans[i][j] = 0;
	}
	
	return ans;
}

inline int** CBaseFunc::new2DIntArr(const int& row, const int& col, const int& val){
	int **ans=new int*[row];
	for(int i=0;i<row;i++){
		ans[i]=new int[col];
		for(int j=0; j<col; j++)
			ans[i][j] = val;
	}
	
	return ans;
}

inline int* CBaseFunc::new1DIntArr(const int& row, const int& val){
	int *ans=new int[row];
	for(int i=0; i<row;i++){
		ans[i] = val;
	}
	
	return ans;
}

inline void CBaseFunc::delete2DIntArr(const int& n, int ** Arr){
	for(int i = 0; i < n; i++){
		delete [] Arr[i];
	}
	delete[] Arr;
	Arr = NULL;
}

inline bool** CBaseFunc::new2DBoolArr(const int& row, const int& col){
	bool **ans=new bool*[row];
	for(int i=0;i<row;i++){
		ans[i]=new bool[col];
		for(int j=0; j<col; j++)
			ans[i][j] = false;
	}
	
	return ans;
}

inline bool** CBaseFunc::new2DBoolArr(const int& row, const int& col, const bool& val){
	bool **ans=new bool*[row];
	for(int i=0;i<row;i++){
		ans[i]=new bool[col];
		for(int j=0; j<col; j++)
			ans[i][j] = val;
	}
	
	return ans;
}

inline bool* CBaseFunc::new1Dbool(const int& row){
	bool* ans = new bool[row];
	for (int i = 0; i < row; i++)
		ans[i] = false;
	return ans;
}

inline void CBaseFunc::delete2DBoolArr(const int& n, bool ** Arr){
	for(int i = 0; i < n; i++){
		delete [] Arr[i];
	}
	delete[] Arr;
	Arr = NULL;
}

/*****************************************************
 * @comments: remove the head and tail spaces
 *****************************************************/
inline string CBaseFunc::stringTrim(const string& str) {
	string ans;
	int start_index = 0;		// inclusive
	int end_index = str.size(); // exclusive
	int i = 0;
	// remove the previous space
	for (start_index = 0; start_index < str.size(); start_index++){
		if (' ' != str[start_index] && '\t' != str[start_index] && '\r' != str[start_index] && '\n' != str[start_index]){
			break;
		}
	}

	for (end_index = str.size(); end_index > start_index; end_index--){
		if (' ' != str[end_index-1] && '\t' != str[end_index-1] && '\r' != str[end_index-1] && '\n' != str[end_index-1]) {
			break;
		}
	}

	for (i = start_index; i < end_index; i++){
		ans += str[i];
	}

	return ans;
}

inline vector<string> CBaseFunc::stringSplit(const string& str, const char& spit){
	int i, size = str.size();
	vector<string> ans;
	vector<char> one;
	for (i = 0; i < size; i++){
		if (spit == str[i]){
			if (one.size() != 0){
				string sub = charVec2String(one);
				ans.push_back(sub);
				vector<char>().swap(one);
			}
		}else{
			one.push_back(str[i]);
		}
	}
	if (one.size() != 0){
		string sub = charVec2String(one);
		ans.push_back(sub);
	}
	
	return ans;
}

inline vector<string> CBaseFunc::stringSplit(const string& str, const char& spit1, const char& spit2){
	int i, size = str.size();
	vector<string> ans;
	vector<char> one;
	for (i = 0; i < size; i++){
		if (spit1 == str[i] || spit2 == str[i]){
			if (one.size() != 0){
				string sub = charVec2String(one);
				ans.push_back(sub);
				vector<char>().swap(one);
			}
		}else{
			one.push_back(str[i]);
		}
	}
	if (one.size() != 0){
		string sub = charVec2String(one);
		ans.push_back(sub);
	}
	
	return ans;
}

inline double CBaseFunc::d0_of_lsscore(const int& Lnorm){
	double d0 = 0.;
	if (Lnorm < 9){
		d0 = 0.1;
	}else{
		d0 = 0.55 * pow(Lnorm - 9, 1.0/3.0) + 0.15;
	}
	
	if (d0 < 0.1)
		d0 = 0.1;
	if (d0 > 4.0)
		d0 = 4.0;
		
	return d0;
} 

inline double CBaseFunc::__2merExchangedSearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max){
	int row_ind, col_ind, iter, exchange_row_ind, exchange_col_ind, new_col_ind, rela_another_row_ind;
	double maxScoreChange, valChange, prev_sco;
	
	double score = prev_score;
	for (iter = 0; iter < iter_max; iter++){
		prev_sco = score;
		if (iter % 2 != 0){
			// direction: 0 -> rownum
			for (row_ind = 0; row_ind < rownum; row_ind++){
				
				col_ind = alivec[row_ind];
				maxScoreChange = 0.;
				exchange_row_ind = -1;
				exchange_col_ind = -1;
				for (new_col_ind = 0; new_col_ind < colnum; new_col_ind++){
					if (new_col_ind == col_ind) continue;
					rela_another_row_ind = transpose_alivec[new_col_ind];
					
					// calculate the changed value 
					valChange = scoMtx[row_ind][new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][new_col_ind] - scoMtx[row_ind][col_ind];
					
					if (-1 != rela_another_row_ind){
						if (-1 != col_ind)
							valChange += scoMtx[rela_another_row_ind][col_ind] - scoMtx[rela_another_row_ind][new_col_ind];
						else valChange -= scoMtx[rela_another_row_ind][new_col_ind];
					}
					
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						exchange_row_ind = rela_another_row_ind;
						exchange_col_ind = new_col_ind;
					}
				}
			
				if (maxScoreChange > 1e-9){
					score += maxScoreChange;
					alivec[row_ind] = exchange_col_ind;
					if (-1 != exchange_row_ind)
						alivec[exchange_row_ind] = col_ind;
						
					if (-1 != exchange_col_ind)
						transpose_alivec[exchange_col_ind] = row_ind;
					if (-1 != col_ind)
						transpose_alivec[col_ind] = exchange_row_ind;
				}
			}//for (row_ind
			
		}else{
			// direction: rownum -> 0 
			for (row_ind = rownum-1; row_ind >= 0; row_ind--){
				col_ind = alivec[row_ind];
				
				maxScoreChange = 0.;
				exchange_row_ind = -1;
				exchange_col_ind = -1;
				for (new_col_ind = 0; new_col_ind < colnum; new_col_ind++){
					if (new_col_ind == col_ind) continue;
					rela_another_row_ind = transpose_alivec[new_col_ind];
					
					// calculate the changed value 
					valChange = scoMtx[row_ind][new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][new_col_ind] - scoMtx[row_ind][col_ind];
					
					if (-1 != rela_another_row_ind){
						if (-1 != col_ind)
							valChange += scoMtx[rela_another_row_ind][col_ind] - scoMtx[rela_another_row_ind][new_col_ind];
						else valChange -= scoMtx[rela_another_row_ind][new_col_ind];
					}
					
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						exchange_row_ind = rela_another_row_ind;
						exchange_col_ind = new_col_ind;
					}
				}
			
				if (maxScoreChange > 1e-9){
					score += maxScoreChange;
					alivec[row_ind] = exchange_col_ind;
					if (-1 != exchange_row_ind)
						alivec[exchange_row_ind] = col_ind;
						
					if (-1 != exchange_col_ind)
						transpose_alivec[exchange_col_ind] = row_ind;
					if (-1 != col_ind)
						transpose_alivec[col_ind] = exchange_row_ind;
				}
			}//for (row_ind
		}
		
		if (fabs(score - prev_sco) < 1e-9) break; 
	}
	
	return score;
}

inline double CBaseFunc::__2merExchangedSearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max){
	int row_ind, col_ind, iter, exchange_row_ind, exchange_col_ind, new_col_ind, rela_another_row_ind;
	double maxScoreChange, valChange, prev_sco;
	
	double score = prev_score;
	for (iter = 0; iter < iter_max; iter++){
		prev_sco = score;
		if (iter % 2 != 0){
			// direction: 0 -> rownum
			for (row_ind = 0; row_ind < rownum; row_ind++){
				
				col_ind = alivec[row_ind];
				maxScoreChange = 0.;
				exchange_row_ind = -1;
				exchange_col_ind = -1;
				for (new_col_ind = 0; new_col_ind < colnum; new_col_ind++){
					if (new_col_ind == col_ind) continue;
					rela_another_row_ind = transpose_alivec[new_col_ind];
					
					// calculate the changed value 
					valChange = scoMtx[row_ind][new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][col_ind]-scoMtx[row_ind][new_col_ind];
					
					if (-1 != rela_another_row_ind){
						if (-1 != col_ind)
							valChange += scoMtx[rela_another_row_ind][new_col_ind]-scoMtx[rela_another_row_ind][col_ind];
						else valChange += scoMtx[rela_another_row_ind][new_col_ind];
					}
					
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						exchange_row_ind = rela_another_row_ind;
						exchange_col_ind = new_col_ind;
					}
				}
			
				if (maxScoreChange > 1e-9){
					score -= maxScoreChange;
					alivec[row_ind] = exchange_col_ind;
					if (-1 != exchange_row_ind)
						alivec[exchange_row_ind] = col_ind;
						
					if (-1 != exchange_col_ind)
						transpose_alivec[exchange_col_ind] = row_ind;
					if (-1 != col_ind)
						transpose_alivec[col_ind] = exchange_row_ind;
				}
			}//for (row_ind
			
		}else{
			// direction: rownum -> 0 
			for (row_ind = rownum-1; row_ind >= 0; row_ind--){
				col_ind = alivec[row_ind];
				
				maxScoreChange = 0.;
				exchange_row_ind = -1;
				exchange_col_ind = -1;
				for (new_col_ind = 0; new_col_ind < colnum; new_col_ind++){
					if (new_col_ind == col_ind) continue;
					rela_another_row_ind = transpose_alivec[new_col_ind];
					
					// calculate the changed value 
					valChange = scoMtx[row_ind][new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][col_ind] - scoMtx[row_ind][new_col_ind];
					
					if (-1 != rela_another_row_ind){
						if (-1 != col_ind)
							valChange += scoMtx[rela_another_row_ind][new_col_ind] - scoMtx[rela_another_row_ind][col_ind];
						else valChange += scoMtx[rela_another_row_ind][new_col_ind];
					}
					
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						exchange_row_ind = rela_another_row_ind;
						exchange_col_ind = new_col_ind;
					}
				}
			
				if (maxScoreChange > 1e-9){
					score -= maxScoreChange;
					alivec[row_ind] = exchange_col_ind;
					if (-1 != exchange_row_ind)
						alivec[exchange_row_ind] = col_ind;
						
					if (-1 != exchange_col_ind)
						transpose_alivec[exchange_col_ind] = row_ind;
					if (-1 != col_ind)
						transpose_alivec[col_ind] = exchange_row_ind;
				}
			}//for (row_ind
		}
		
		if (fabs(score - prev_sco) < 1e-9) break; 
	}
	
	return score;
}

inline double CBaseFunc::__3merExchangedSearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max){
	int iter, row_ind, col_ind, jth_exchange_row_ind, jth_exchange_col_ind, kth_exchange_row_ind, kth_exchange_col_ind,
			 jth_new_col_ind, jth_rela_another_row_ind, kth_new_col_ind, kth_rela_another_row_ind;
	double maxScoreChange, valChange, prev_sco;
	
	double score = prev_score;
	for (iter = 0; iter < iter_max; iter++){
		prev_sco = score;
		for (row_ind = 0; row_ind < rownum; row_ind++){
			col_ind = alivec[row_ind];
			
			maxScoreChange = 0.;
			jth_exchange_row_ind = -1;
			jth_exchange_col_ind = -1;
			kth_exchange_row_ind = -1;
			kth_exchange_col_ind = -1;
			for (jth_new_col_ind = 0; jth_new_col_ind < colnum; jth_new_col_ind++){ // j does not mean the column index
				if (jth_new_col_ind == col_ind) continue;
				jth_rela_another_row_ind = transpose_alivec[jth_new_col_ind];
				if (-1 == jth_rela_another_row_ind) continue;
					
				for (kth_new_col_ind = 0; kth_new_col_ind < colnum; kth_new_col_ind++){// k does not mean the column index
					if (kth_new_col_ind == col_ind || kth_new_col_ind == jth_new_col_ind) continue;
					kth_rela_another_row_ind = transpose_alivec[kth_new_col_ind];
							
					// calculate the changed value
					valChange = scoMtx[row_ind][jth_new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][jth_new_col_ind] - scoMtx[row_ind][col_ind];
								
					valChange += scoMtx[jth_rela_another_row_ind][kth_new_col_ind] - scoMtx[jth_rela_another_row_ind][jth_new_col_ind];
							
					if (-1 != kth_rela_another_row_ind){
						if (-1 != col_ind)
								valChange += scoMtx[kth_rela_another_row_ind][col_ind] - scoMtx[kth_rela_another_row_ind][kth_new_col_ind];
						else valChange -= scoMtx[kth_rela_another_row_ind][kth_new_col_ind];
					}
							
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						jth_exchange_row_ind = jth_rela_another_row_ind;
						jth_exchange_col_ind = jth_new_col_ind;
						kth_exchange_row_ind = kth_rela_another_row_ind;
						kth_exchange_col_ind = kth_new_col_ind;
					}
				}// for_k
			}//for_j
			
			if (maxScoreChange > 1e-9){
				score += maxScoreChange;
				
				if (scoMtx[row_ind][jth_exchange_col_ind] > 1e-9) {
					alivec[row_ind] = jth_exchange_col_ind;
					transpose_alivec[jth_exchange_col_ind] = row_ind;
				}else {
					alivec[row_ind] = -1;
					transpose_alivec[jth_exchange_col_ind] = -1;
				}
				
				if (scoMtx[jth_exchange_row_ind][kth_exchange_col_ind] > 1e-9) {
					alivec[jth_exchange_row_ind] = kth_exchange_col_ind;
					transpose_alivec[kth_exchange_col_ind] = jth_exchange_row_ind;
				}else {
					alivec[jth_exchange_row_ind] = -1;
					transpose_alivec[kth_exchange_col_ind] = -1;
				}
				
				if (-1 != kth_exchange_row_ind)
					if (-1 == col_ind || scoMtx[kth_exchange_row_ind][col_ind] <= 1e-9)
						alivec[kth_exchange_row_ind] = -1;
					else alivec[kth_exchange_row_ind] = col_ind;
						
				if (-1 != col_ind)
					if (-1 == kth_exchange_row_ind || scoMtx[kth_exchange_row_ind][col_ind] <= 1e-9)
						transpose_alivec[col_ind] = -1;
					else transpose_alivec[col_ind] = kth_exchange_row_ind;
				
//					System.out.println("=============================================================");
//					double sum = 0;
//					for (int i = 0; i < alivec.length; i++) {
//						if (-1 != alivec[i]) {
//							System.out.println(i + " : " + alivec[i] + " : " + scoMtx[i][alivec[i]]);
//							sum += scoMtx[i][alivec[i]];
//						}
//					}
//					System.out.println("sum = " + sum + ", score = " + score + ", " + maxScoreChange);
			}
		}//for (row_ind
		
		if (fabs(score - prev_sco) < 1e-9) break; 
	}
	
	return score;
}

inline double CBaseFunc::__3merExchangedSearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec, const double& prev_score, const int& iter_max){
	int iter, row_ind, col_ind, jth_exchange_row_ind, jth_exchange_col_ind, kth_exchange_row_ind, kth_exchange_col_ind,
			 jth_new_col_ind, jth_rela_another_row_ind, kth_new_col_ind, kth_rela_another_row_ind;
	double maxScoreChange, valChange, prev_sco;
	
	double score = prev_score;
	for (iter = 0; iter < iter_max; iter++){
		prev_sco = score;
		for (row_ind = 0; row_ind < rownum; row_ind++){
			col_ind = alivec[row_ind];
			
			maxScoreChange = 0.;
			jth_exchange_row_ind = -1;
			jth_exchange_col_ind = -1;
			kth_exchange_row_ind = -1;
			kth_exchange_col_ind = -1;
			for (jth_new_col_ind = 0; jth_new_col_ind < colnum; jth_new_col_ind++){ // j does not mean the column index
				if (jth_new_col_ind == col_ind) continue;
				jth_rela_another_row_ind = transpose_alivec[jth_new_col_ind];
				if (-1 == jth_rela_another_row_ind) continue;
					
				for (kth_new_col_ind = 0; kth_new_col_ind < colnum; kth_new_col_ind++){// k does not mean the column index
					if (kth_new_col_ind == col_ind || kth_new_col_ind == jth_new_col_ind) continue;
					kth_rela_another_row_ind = transpose_alivec[kth_new_col_ind];
							
					// calculate the changed value
					valChange = scoMtx[row_ind][jth_new_col_ind];
					if (-1 != col_ind)
						valChange = scoMtx[row_ind][col_ind] - scoMtx[row_ind][jth_new_col_ind];
								
					valChange += scoMtx[jth_rela_another_row_ind][jth_new_col_ind] - scoMtx[jth_rela_another_row_ind][kth_new_col_ind];
							
					if (-1 != kth_rela_another_row_ind){
						if (-1 != col_ind)
								valChange += scoMtx[kth_rela_another_row_ind][kth_new_col_ind] - scoMtx[kth_rela_another_row_ind][col_ind];
						else valChange += scoMtx[kth_rela_another_row_ind][kth_new_col_ind];
					}
							
					if (valChange > maxScoreChange){
						maxScoreChange = valChange;
						jth_exchange_row_ind = jth_rela_another_row_ind;
						jth_exchange_col_ind = jth_new_col_ind;
						kth_exchange_row_ind = kth_rela_another_row_ind;
						kth_exchange_col_ind = kth_new_col_ind;
					}
				}// for_k
			}//for_j
			
			if (maxScoreChange > 1e-9){
				score -= maxScoreChange;
				
				if (scoMtx[row_ind][jth_exchange_col_ind] > 1e-9) {
					alivec[row_ind] = jth_exchange_col_ind;
					transpose_alivec[jth_exchange_col_ind] = row_ind;
				}else {
					alivec[row_ind] = -1;
					transpose_alivec[jth_exchange_col_ind] = -1;
				}
				
				if (scoMtx[jth_exchange_row_ind][kth_exchange_col_ind] > 1e-9) {
					alivec[jth_exchange_row_ind] = kth_exchange_col_ind;
					transpose_alivec[kth_exchange_col_ind] = jth_exchange_row_ind;
				}else {
					alivec[jth_exchange_row_ind] = -1;
					transpose_alivec[kth_exchange_col_ind] = -1;
				}
				
				if (-1 != kth_exchange_row_ind)
					if (-1 == col_ind || scoMtx[kth_exchange_row_ind][col_ind] <= 1e-9)
						alivec[kth_exchange_row_ind] = -1;
					else alivec[kth_exchange_row_ind] = col_ind;
						
				if (-1 != col_ind)
					if (-1 == kth_exchange_row_ind || scoMtx[kth_exchange_row_ind][col_ind] <= 1e-9)
						transpose_alivec[col_ind] = -1;
					else transpose_alivec[col_ind] = kth_exchange_row_ind;
				
//					System.out.println("=============================================================");
//					double sum = 0;
//					for (int i = 0; i < alivec.length; i++) {
//						if (-1 != alivec[i]) {
//							System.out.println(i + " : " + alivec[i] + " : " + scoMtx[i][alivec[i]]);
//							sum += scoMtx[i][alivec[i]];
//						}
//					}
//					System.out.println("sum = " + sum + ", score = " + score + ", " + maxScoreChange);
			}
		}//for (row_ind
		
		if (fabs(score - prev_sco) < 1e-9) break; 
	}
	
	return score;
}

// Please make sure that rownum > colnum, it will save several seconds O(n^3)
// all element in scoMtx should be zero or positive number, disconnect should be set to zero.
// this program will find the highest score sum corresponded alignment
inline double CBaseFunc::greedySearch(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec){
	int i, corrRowInd, corrColInd, colInd, rr, cc;
	double maxValue, value;
	
	for (i = 0; i < rownum; i++) alivec[i] = -1;
	for (i = 0; i < colnum; i++) transpose_alivec[i] = -1;
	
	int minnum = rownum > colnum ? colnum : rownum;
	double score = 0.0;
	for (i = 0; i < minnum; i++){	// i means the ith alignment, not row index
		maxValue = 0.0;
		corrRowInd = -1;
		corrColInd = -1;
		for (rr = 0; rr < rownum; rr++){	// rr means the rr-th row in rowSortedInds
			if (-1 == alivec[rr]){
				colInd = -1;
				value = 0.;
				for (cc = 0; cc < colnum; cc++){
					if (-1 == transpose_alivec[cc] && value < scoMtx[rr][cc]){
						colInd = cc;
						value = scoMtx[rr][cc];
					}
				}
					
				if (maxValue < value){
					maxValue = value;
					corrRowInd = rr;
					corrColInd = colInd;
				}
			}
		}
		
		score += maxValue;
		if (-1 != corrRowInd)
			alivec[corrRowInd] = corrColInd;
		if (-1 != corrColInd)
			transpose_alivec[corrColInd] = corrRowInd;
	}
	
	return score;
}

// Please make sure that rownum > colnum, it will save several seconds O(n^3)
// all element in scoMtx should be zero or positive number, disconnect should be set to INF.
// this program will find the smallest score sum corresponded alignment
inline double CBaseFunc::greedySearchMinimum(double** scoMtx, const int& rownum, const int& colnum, int* alivec, int* transpose_alivec){
	int i, corrRowInd, corrColInd, colInd, rr, cc;
	double minValue, value;
	
	for (i = 0; i < rownum; i++) alivec[i] = -1;
	for (i = 0; i < colnum; i++) transpose_alivec[i] = -1;
	
	int minnum = rownum > colnum ? colnum : rownum;
	double score = 0.0;
	for (i = 0; i < minnum; i++){	// i means the ith alignment, not row index
		minValue = g_inf;
		corrRowInd = -1;
		corrColInd = -1;
		for (rr = 0; rr < rownum; rr++){	// rr means the rr-th row in rowSortedInds
			if (-1 == alivec[rr]){
				colInd = -1;
				value = g_inf;
				for (cc = 0; cc < colnum; cc++){
					if (-1 == transpose_alivec[cc] && value > scoMtx[rr][cc]){
						colInd = cc;
						value = scoMtx[rr][cc];
					}
				}
					
				if (minValue > value){
					minValue = value;
					corrRowInd = rr;
					corrColInd = colInd;
				}
			}
		}
		
		score += minValue;
		if (-1 != corrRowInd)
			alivec[corrRowInd] = corrColInd;
		if (-1 != corrColInd)
			transpose_alivec[corrColInd] = corrRowInd;
	}
	
	return score;
}


inline Ligand::Ligand(const string& path, const INPUT_FILE_TYPE& input_file_type, const bool& is_load_H, const bool& is_care_bond_type) {
	if (PDB == input_file_type)
		load_from_pdb(path, is_load_H);
	else if (MOL2 == input_file_type)
		load_from_mol2(path, is_load_H, is_care_bond_type);
	else if (SDF == input_file_type){
		load_from_sdf(path, is_load_H, is_care_bond_type);
	}
}

// See SDF format in https://www.nonlinear.com/progenesis/sdf-studio/v0.9/faq/sdf-file-format-guidance.aspx
inline void Ligand::load_from_sdf(const string& path, const bool& is_load_H, const bool& is_care_bond_type){
	bt_mtx = NULL;
	
	char cstr[50];
	
	//========================================================
	// load file contents
	//========================================================
	vector<string>* contents = new vector<string>();
	{
		string line;
		ifstream fin(path.c_str());
		while (getline(fin, line))
			contents->push_back(line);
		fin.close();
	}
	
	int __size = contents->size();
	if (__size < 5){
		cout << path << " is not normal sdf format file." << endl;
		cout << "Please check it!" << endl;
		exit(-1);
	}
	
	string s = (*contents)[3];
	
	int atom_num = 0;
	int bond_num = 0;
		
	strcpy(cstr, (s.substr(0, 3)).c_str());	
	sscanf(cstr, "%d", &atom_num);
	strcpy(cstr, (s.substr(3, 6)).c_str());
	sscanf(cstr, "%d", &bond_num);
	
	if (__size < 4+atom_num+bond_num){
		cout << path << " is not normal sdf format file." << endl;
		cout << "Please check it!" << endl;
		exit(-1);
	}
	
	double x, y, z;
	double* xyz = NULL;
	int atomind; 
	string atomtype;
	string atomsimpletype;
	
	map<int, int> oind_nind_for_care_atoms;
	int oind_for_care_atom = 0;
	int nind_for_care_atom = 0;
	int end_ind = 4+atom_num;
	for (int i = 4; i < end_ind; i++){
		s = (*contents)[i];
		
		if (s.length() < 33){
			cout << path << " is not normal sdf format file." << endl;
			cout << "Please check it!" << endl;
			exit(-1);
		}
		
		strcpy(cstr, s.substr(0, 10).c_str());
		sscanf(cstr, "%lf", &x);
		strcpy(cstr, s.substr(10, 10).c_str());
		sscanf(cstr, "%lf", &y);
		strcpy(cstr, s.substr(20, 10).c_str());
		sscanf(cstr, "%lf", &z);
		
		xyz = new double[3];
		xyz[0] = x;
		xyz[1] = y;
		xyz[2] = z;
		
		atomind = i-3; // -4+1
		atomtype = CBaseFunc::stringTrim(s.substr(30, 3));
		atomsimpletype = atomtype;
		
		if (is_load_H || atomsimpletype != "H"){
			m_cared_xyz_vec.push_back(xyz);
			
			m_cared_atom_orig_ind_vec.push_back(atomind);
			
			CBaseFunc::toUpperString(atomtype);
			m_cared_atomtype_vec.push_back(atomtype);
			
			CBaseFunc::toUpperString(atomsimpletype);
			m_cared_atomsimpletype_vec.push_back(atomsimpletype);
			
			oind_nind_for_care_atoms[oind_for_care_atom] = nind_for_care_atom;
			nind_for_care_atom++;
		}
		oind_for_care_atom++;
	}
	
	int atomnum = m_cared_xyz_vec.size();
	if (atomnum < 1){
		cout << path << " is not normal mol2 format file." << endl;
		cout << "Please check it!" << endl;
		exit(-1);
	}
	
	this->bt_mtx = new CHEMICAL_BOND_TYPE*[atomnum];
	for (int i = 0; i < atomnum; i++){
		this->bt_mtx[i] = new CHEMICAL_BOND_TYPE[atomnum];
		for (int j = 0; j < atomnum; j++){
			this->bt_mtx[i][j] = NOTCONNECTED;
		}
	}
	
	int atom1oind, atom2oind;
	int atom1nind, atom2nind;
	end_ind = 4+atom_num+bond_num;
	for (int i = 4+atom_num; i < bond_num; i++){
		s = (*contents)[i];
		
		vector<string> llc = CBaseFunc::stringSplit(s, ' ', '\t');
		if (llc.size() < 4)
			continue;
			
		sscanf(llc[0].c_str(), "%d", &atom1oind);
		atom1oind--;
		sscanf(llc[1].c_str(), "%d", &atom2oind);
		atom2oind--;
		
		if (oind_nind_for_care_atoms.end() == oind_nind_for_care_atoms.find(atom2oind)
			|| oind_nind_for_care_atoms.end() == oind_nind_for_care_atoms.find(atom1oind))
			continue;
		
		atom1nind = oind_nind_for_care_atoms[atom1oind];
		atom2nind = oind_nind_for_care_atoms[atom2oind];
		
		CHEMICAL_BOND_TYPE bondtype = SINGLE;
		if (is_care_bond_type){
			if (llc[2].size() == 1 && llc[2].compare(0, 1, "1")==0){
				bondtype = SINGLE;
			}else if (llc[2].size() == 1 && llc[2].compare(0, 1, "2")==0){
				bondtype = DOUBLE;
			}else if (llc[2].size() == 1 && llc[2].compare(0, 1, "3")==0){
				bondtype = TRIPLE;
			}else if (llc[2].size() == 2 && llc[2].compare(0, 2, "4")==0){
				bondtype = AROMATIC;	
			}else {
				bondtype = DONOTKNOW;
			}	
		}
		
		this->bt_mtx[atom1nind][atom2nind] = this->bt_mtx[atom2nind][atom1nind] = bondtype;	
	}
	
	vector<string>().swap(*contents);
	delete contents; 
}

inline void Ligand::load_from_mol2(const string& path, const bool& is_load_H, const bool& is_care_bond_type){
	bt_mtx = NULL;
	
	//========================================================
	// load file contents
	//========================================================
	vector<string>* contents = new vector<string>();
	{
		string line;
		ifstream fin(path.c_str());
		while (getline(fin, line))
			contents->push_back(line);
		fin.close();
	}
	const vector<string>& oneLigMol2Infos = *contents;
	
	int __size = oneLigMol2Infos.size();
	int l = 0;
	while (l < __size && oneLigMol2Infos[l].compare(0, 13, "@<TRIPOS>ATOM") != 0)
		l++;
	l++;
	
	double x, y, z;
	double* xyz = NULL;
	int atomind; 
	string atomtype;
	string atomsimpletype;
	
	char cstr[50];
	int dot_ind;
	map<int, int> oind_nind_for_care_atoms;
	int oind_for_care_atom = 0;
	int nind_for_care_atom = 0;
	while (l < __size){
		if (oneLigMol2Infos[l].compare(0, 9, "@<TRIPOS>") == 0)
			break;
		
		vector<string> llc = CBaseFunc::stringSplit(oneLigMol2Infos[l], ' ', '\t');
		if (llc.size() < 6)
			continue;
		
		strcpy(cstr, llc[2].c_str());
		sscanf(cstr, "%lf", &x);
		strcpy(cstr, llc[3].c_str());
		sscanf(cstr, "%lf", &y);
		strcpy(cstr, llc[4].c_str());
		sscanf(cstr, "%lf", &z);
		
		xyz = new double[3];
		xyz[0] = x;
		xyz[1] = y;
		xyz[2] = z;
		
		strcpy(cstr, llc[0].c_str());
		sscanf(cstr, "%d", &atomind);

		atomtype = llc[1];

		atomsimpletype = llc[5];
		dot_ind = atomsimpletype.find(".");
		if (string::npos != dot_ind)
			atomsimpletype = atomsimpletype.substr(0, dot_ind);
		
		if (is_load_H || atomsimpletype != "H"){
			m_cared_xyz_vec.push_back(xyz);
			
			m_cared_atom_orig_ind_vec.push_back(atomind);
			
			CBaseFunc::toUpperString(atomtype);
			m_cared_atomtype_vec.push_back(atomtype);
			
			CBaseFunc::toUpperString(atomsimpletype);
			m_cared_atomsimpletype_vec.push_back(atomsimpletype);
			
			oind_nind_for_care_atoms[oind_for_care_atom] = nind_for_care_atom;
			nind_for_care_atom++;
		}
		oind_for_care_atom++;
		l++;
	}
	
	int atomnum = m_cared_xyz_vec.size();
	if (atomnum < 1){
		cout << path << " is not normal mol2 format file." << endl;
		cout << "Please check it!" << endl;
		exit(-1);
	}
	
	this->bt_mtx = new CHEMICAL_BOND_TYPE*[atomnum];
	for (int i = 0; i < atomnum; i++){
		this->bt_mtx[i] = new CHEMICAL_BOND_TYPE[atomnum];
		for (int j = 0; j < atomnum; j++){
			this->bt_mtx[i][j] = NOTCONNECTED;
		}
	}
	
	int ll = l;
	while (ll < oneLigMol2Infos.size() && oneLigMol2Infos[ll].compare(0, 13, "@<TRIPOS>BOND") != 0)
		ll++;
	ll++;
	
	int atom1oind, atom2oind;
	int atom1nind, atom2nind;
	while (ll < __size){
		if (oneLigMol2Infos[ll].compare(0, 9, "@<TRIPOS>") == 0)
			break;
		
		vector<string> llc = CBaseFunc::stringSplit(oneLigMol2Infos[ll], ' ', '\t');
		if (llc.size() < 4){
			ll++;
			continue;
		}
		
		sscanf(llc[1].c_str(), "%d", &atom1oind);
		atom1oind--;
		sscanf(llc[2].c_str(), "%d", &atom2oind);
		atom2oind--;
		
		if (oind_nind_for_care_atoms.end() == oind_nind_for_care_atoms.find(atom2oind)
			|| oind_nind_for_care_atoms.end() == oind_nind_for_care_atoms.find(atom1oind)){
			ll++;
			continue;
		}
		
		atom1nind = oind_nind_for_care_atoms[atom1oind];
		atom2nind = oind_nind_for_care_atoms[atom2oind];
		
		CHEMICAL_BOND_TYPE bondtype = SINGLE;
		if (is_care_bond_type){
			if (llc[3].size() == 1 && llc[3].compare(0, 1, "1")==0){
				bondtype = SINGLE;
			}else if (llc[3].size() == 1 && llc[3].compare(0, 1, "2")==0){
				bondtype = DOUBLE;
			}else if (llc[3].size() == 1 && llc[3].compare(0, 1, "3")==0){
				bondtype = TRIPLE;
			}else if (llc[3].size() == 2 && llc[3].compare(0, 2, "am")==0){
				bondtype = AMIDE;		
			}else if (llc[3].size() == 2 && llc[3].compare(0, 2, "ar")==0){
				bondtype = AROMATIC;	
			}else if (llc[3].size() == 2 && llc[3].compare(0, 2, "du")==0){
				bondtype = DUMMY;		
			}
		}
		
		this->bt_mtx[atom1nind][atom2nind] = this->bt_mtx[atom2nind][atom1nind] = bondtype;
		ll++;
	}
	
	vector<string>().swap(*contents);
	delete contents; 
}

inline void Ligand::load_from_pdb(const string& path, const bool& is_load_H){
	bt_mtx = NULL;
	
	//========================================================
	// load PDB file contents
	//========================================================
	vector<string>* contents = new vector<string>();
	{
		string line;
		// load all atom lines in pdb
		ifstream fin(path.c_str());
		while (getline(fin, line)) {
			//just load the first model
			if (0 == line.compare(0, 3, "END")) break;
			//load all atom and hetatm lines
			if (0 == line.compare(0, 4, "ATOM") || 0 == line.compare(0, 6, "HETATM"))
				contents->push_back(line);
		}
		fin.close();
	}
	
	int size = contents->size();
	int line = 0;
	int llen; 
	string lline;
	double x, y, z;
	double* xyz = NULL;
	char cstr[50];
	int atomind; 
	string atomtype;
	string atomsimpletype;
	
	while (size > line){
		lline = (*contents)[line];
		llen = lline.size();
		
		if (llen < 54) {
			line++;
			continue;
		}
				
		strcpy(cstr, (lline.substr(30, 8)).c_str());
		sscanf(cstr, "%lf", &x);
		strcpy(cstr, (lline.substr(38, 8)).c_str());
		sscanf(cstr, "%lf", &y);
		strcpy(cstr, (lline.substr(46, 8)).c_str());
		sscanf(cstr, "%lf", &z);
		
		xyz = new double[3];
		xyz[0] = x;
		xyz[1] = y;
		xyz[2] = z;
		
		strcpy(cstr, (lline.substr(6, 5)).c_str());
		sscanf(cstr, "%d", &atomind);
		
		atomtype = CBaseFunc::stringTrim(lline.substr(12, 4));
		atomsimpletype = CBaseFunc::stringTrim(lline.substr(76, 2));
		if (is_load_H || atomsimpletype != "H"){
			m_cared_xyz_vec.push_back(xyz);
			
			m_cared_atom_orig_ind_vec.push_back(atomind);
			
			CBaseFunc::toUpperString(atomtype);
			m_cared_atomtype_vec.push_back(atomtype);
			
			CBaseFunc::toUpperString(atomsimpletype);
			m_cared_atomsimpletype_vec.push_back(atomsimpletype);
		}
		
		line++;
	}
	
	vector<string>().swap(*contents);
	delete contents; 
	
	int __size = m_cared_xyz_vec.size();
	bt_mtx = new CHEMICAL_BOND_TYPE*[__size];
	for (int i = 0; i < __size; i++){
		bt_mtx[i] = new CHEMICAL_BOND_TYPE[__size];
		for (int j = 0; j < __size; j++){
			bt_mtx[i][j] = DONOTKNOW;
		}
	}
}

inline const double* Ligand::operator [] (const int& i) {
	return m_cared_xyz_vec[i];
}

inline const int Ligand::size() {
	return m_cared_xyz_vec.size();
}

inline Ligand::~Ligand() {
	int i;
	int __size = m_cared_xyz_vec.size();
	if (NULL != bt_mtx){
		for (i = 0; i < __size; i++)
			delete[] bt_mtx[i];
		delete[] bt_mtx;
	}
	
	for (i = 0; i < __size; i++){
		delete[] m_cared_xyz_vec[i];	
	}
	vector<double*>().swap(m_cared_xyz_vec);
	
	vector<string>().swap(this->m_cared_atomtype_vec);
}

inline bool CBaseFunc::is_same(const vector<char>& a, const vector<char>& b){
	int i, n = a.size();
	bool ans = true;
	if (n != b.size())
		ans = false;
	else{
		for (i = 0; i < n; i++){
			if (a[i] != b[i]){
				ans = false;
				break;				
			}
		}	
	}
	
	return ans;
}

inline const vector<double*>& Ligand::get_cared_xyz_vec(){
	return this->m_cared_xyz_vec;
}

inline const int& Ligand::get_ith_cared_atom_orig_index(const int& i){
	return this->m_cared_atom_orig_ind_vec[i];
}

inline const double& CDockEvaluator::get_lsscore(){
	return this->lsscore;
}

inline unsigned long long CBaseFunc::factorial(const int& n){
	unsigned long long result = 1;  
    for (int i = 1; i <= n; i++)
        result *= i;  
    return result;  
}

inline double CBaseFunc::distance2(const double* a, const double* b){
	double xbias = a[0] - b[0];
	double ybias = a[1] - b[1];
	double zbias = a[2] - b[2];
	return xbias*xbias + ybias*ybias + zbias*zbias;
}

inline void CDockEvaluator::print_result(){
	int i, j, n;
	int qatnum = query->size();
	int tatnum = templ->size();
	
	char buf[5000];
	sprintf(buf, "Structure 1: %d heavy atom number.", qatnum);
	cout << buf << endl; 
	sprintf(buf, "Structure 2: %d heavy atom number.", tatnum);
	cout << buf << endl << endl;
	
	sprintf(buf, "RMSD: %8.6f", this->rmsd);
	cout << buf << endl;
	
	sprintf(buf, "LS-score: %8.6f (d0 = %8.6f)", this->lsscore, this->d0);
	cout << buf << endl << endl;

	cout << "------------------------------------------------" << endl;
	cout << "Detail Distance information of the best mapping:" << endl;
	cout << "------------------------------------------------" << endl;
	cout << "         Structure 1                Structure 2 " << endl;
	cout << "        -------------              -------------" << endl;
	cout << "ind.    oind.   atype   distance   oind.   atype" << endl;  
	cout << "------------------------------------------------" << endl;
	
	n = this->aa_level_ali.size();
	bool* is_used = CBaseFunc::new1Dbool(n);
	for (i = 0; i < n; i++){
		for (j = 0; j < n; j++){
			if (is_used[j]) continue;
			ALIGN_PAIR ap = this->aa_level_ali[j];
			if (ap.qind != i) continue;
			
			double dis = sqrt(ap.dis2);
			if (dis < 10.){
				sprintf(buf, "%4d    %5d    %4s   %8.6f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());			
			}else if (dis < 100){
				sprintf(buf, "%4d    %5d    %4s   %8.5f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());
			}else if (dis < 1000){
				sprintf(buf, "%4d    %5d    %4s   %8.4f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());			
			}else if (dis < 10000){
				sprintf(buf, "%4d    %5d    %4s   %8.3f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());			
			}else if (dis < 100000){
				sprintf(buf, "%4d    %5d    %4s   %8.2f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());
			}else if (dis < 1000000){
				sprintf(buf, "%4d    %5d    %4s   %8.1f   %5d    %4s", 
						i+1, ap.qoind, ap.qaa.c_str(), dis, ap.toind, ap.taa.c_str());			
			}
			cout << buf << endl;
			is_used[j] = true;
		}
	}
	
	cout << "--------------------------------------------------" << endl;
	cout << "* 'oind': Atom index in input file" << endl;
	cout << "* 'atype': Atom type in input file" << endl;
	cout << "--------------------------------------------------" << endl;
	
	cout << endl << endl;
}


inline vector<string> CBaseFunc::string2stringVec(const string& str){
	vector<string> ans;
	int n = str.size();
	for (int i = 0; i < n; i++){
		ans.push_back(str.substr(i, i+1));
	}
	
	return ans;
}

inline void CBaseFunc::toUpperString(string &str){
   transform(str.begin(), str.end(), str.begin(), (int (*)(int))toupper);  
}

inline string CBaseFunc::eraseAll(const string &str, char ch){
    string s(str.c_str());
    int index = 0;
    if( !s.empty())
    {
        while( (index = s.find(ch, index)) != string::npos)
        {
            s.erase(index,1);
        }
    }
		
		return s;
}

inline string CBaseFunc::eraseAll(const string &str, const char* arr, int len){
    string s(str.c_str());
    for (int i = 0; i < len; i++){
		s = eraseAll(s, arr[i]);
	}
	return s;
}

inline int*** CBaseFunc::new3DIntArr(int row, int col, int thd){
	int ***ans=new int**[row];
	for(int i=0;i<row;i++){
		ans[i]=new int*[col];
		for (int j=0; j<col;j++){
			ans[i][j]=new int[thd];
			for (int k=0; k<thd; k++){
				ans[i][j][k] = 0;
			}
		}
	}
	
	return ans;
}

inline int*** CBaseFunc::new3DIntArr(int row, int col, int thd, int val){
	int ***ans=new int**[row];
	for(int i=0;i<row;i++){
		ans[i]=new int*[col];
		for (int j=0; j<col;j++){
			ans[i][j]=new int[thd];
			for (int k=0; k<thd; k++){
				ans[i][j][k] = val;
			}
		}
	}
	
	return ans;
}

inline const string& Ligand::get_cared_atomsimpletype_in_lig(const int& i){
	return m_cared_atomsimpletype_vec[i];
}

inline const vector<string>& Ligand::get_cared_atomtype_vec_in_lig(){
	return m_cared_atomtype_vec;
}

inline const CHEMICAL_BOND_TYPE Ligand::get_chemical_bond_type(const int& i, const int& j){
	if (NULL == this->bt_mtx)
		return DONOTKNOW;
	
	return this->bt_mtx[i][j];
} 

inline void CBaseFunc::delete3DIntArr(int row, int col, int*** Arr){
	for(int i = 0; i < row; i++){
		for (int j = 0; j < col; j++){
			delete[] Arr[i][j];
		}
		delete[] Arr[i];
	}
	delete[] Arr;
	Arr = NULL;
}

inline bool LigAtomMatcher::is_simple_same_important(LigAtomMatcher& ilam, int& i, LigAtomMatcher& jlam, int& j){
	const string& iat = ilam.get_ith_at(i);
	const string& jat = jlam.get_ith_at(j);
	if (iat != jat)
		return false;
	
	const vector<CHEMICAL_BOND_TYPE>& icbts = ilam.get_ith_cbts(i);
	const vector<CHEMICAL_BOND_TYPE>& jcbts = jlam.get_ith_cbts(j);
	int ilen = icbts.size();
	int jlen = jcbts.size();
	if (ilen != jlen)
		return false;
	
	const vector<string>& inats = ilam.get_ith_nats(i);
	const vector<string>& jnats = jlam.get_ith_nats(j);
	int in = inats.size();
	int jn = jnats.size();
	if (in != jn)
		return false;
		
	int k, l;
	bool is_matched, ans = true;
	{
		bool* is_used = CBaseFunc::new1Dbool(jlen);
		for (k = 0; k < ilen; k++){
			is_matched = false;
			for (l = 0; l < jlen; l++){
				if (is_used[l]) continue;
				if (icbts[k] == jcbts[l]){
					is_matched = true;
					is_used[l] = true;
					break;
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		delete[] is_used; 
	}
	
	if (ans){
		bool* is_used = CBaseFunc::new1Dbool(jn);
		for (k = 0; k < in; k++){
			is_matched = false;
			for (l = 0; l < jn; l++){
				if (is_used[l]) continue;
				if (inats[k] == jnats[l]){
					is_matched = true;
					is_used[l] = true;
					break;						
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		delete[] is_used; 
	}
	
	return ans;
}

inline bool LigAtomMatcher::is_same_road(LigAtomMatcher& qlam, int& qi, int& qj, LigAtomMatcher& tlam, int& ti, int& tj, bool** is_same_important_mtx_between_ilam_and_jlam){
	const SIMPLE_ROAD* qr = qlam.get_ij_simple_road(qi, qj);
	const SIMPLE_ROAD* tr = tlam.get_ij_simple_road(ti, tj);
	if (qr->roadlen!=tr->roadlen 
			|| !is_same_important_mtx_between_ilam_and_jlam[qr->start_atind][tr->start_atind]
			|| !is_same_important_mtx_between_ilam_and_jlam[qr->end_atind][tr->end_atind]){
				return false;
	}
	
	return true;
}

inline bool LigAtomMatcher::is_same_important(LigAtomMatcher& ilam, int& i, LigAtomMatcher& jlam, int& j, bool** is_simple_important_mtx_between_ilam_and_jlam){
	if (!is_simple_important_mtx_between_ilam_and_jlam[i][j])
		return false;
	
	const vector<SIMPLE_ROAD* >& irvec = ilam.get_ith_simple_roads(i);
	const vector<SIMPLE_ROAD* >& jrvec = jlam.get_ith_simple_roads(j);
	
	int ilen = irvec.size();
	int jlen = jrvec.size();
	if (ilen == jlen){
		double is_matched, ans = true;
		bool* is_used = CBaseFunc::new1Dbool(jlen);
		for (int k = 0; k < ilen; k++){
			SIMPLE_ROAD& ir = *irvec[k];
			is_matched = false;
			for (int l = 0; l < jlen; l++) {
				if (is_used[l]) continue;
				SIMPLE_ROAD& jr = *jrvec[l];
				if (ir.roadlen==jr.roadlen && is_simple_important_mtx_between_ilam_and_jlam[ir.end_atind][jr.end_atind]){
					is_matched = true;
					is_used[l] = true;
					break;
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		
		delete[] is_used;
		return ans;
	}else return false;
}

inline const string& LigAtomMatcher::get_ith_at(const int& i) {
	return this->ats[i]; 
}

inline const vector<CHEMICAL_BOND_TYPE>& LigAtomMatcher::get_ith_cbts(const int& i) {
	return this->cbtss[i];
}

inline const vector<string>& LigAtomMatcher::get_ith_nats(const int& i) {
	return this->natss[i]; 
}

inline const vector<SIMPLE_ROAD* >& LigAtomMatcher::get_ith_simple_roads(const int& i){
	return *(this->attypes_in_roads[i]);
}

inline const SIMPLE_ROAD* LigAtomMatcher::get_ij_simple_road(const int& i, const int& j){
	return (*(this->attypes_in_roads[i]))[j];
}

inline void LigAtomMatcher::extract_atgs() {
	int i, j, k, n, m;
	
	vector<vector<int> > __atgs; // buf atom groups 
	bool is_new_group;
	for (i = 0; i < atnum; i++){
		is_new_group = true;
		n = __atgs.size();
		for (k = 0; k < n; k++){
			vector<int>& kth_atg = __atgs[k];
			if (is_same_important(kth_atg[0], i)){
				kth_atg.push_back(i);
				is_new_group = false;
				break;
			}
		}
		
		if (is_new_group){
			vector<int> atg;
			atg.push_back(i);
			__atgs.push_back(atg);
		}
	}
	
	int __atgs_size = __atgs.size();
	vector<int> one_atom_group_vec;
	vector<vector<int> > multi_atgs;
	for (i = 0; i < __atgs_size; i++){
		if (1 == __atgs[i].size()){
			one_atom_group_vec.push_back(__atgs[i][0]);
			
			vector<int>* p_atg = new vector<int>();
			p_atg->push_back(__atgs[i][0]);
			atgs.push_back(p_atg);
		}else multi_atgs.push_back(__atgs[i]);	
	}
	vector<vector<int> > buf_multi_atgs;
	
	int one_atom_group_vec_size = one_atom_group_vec.size();
	int multi_atgs_size = multi_atgs.size();
	while (one_atom_group_vec_size > 0 && multi_atgs_size > 0) {
		int one_atom_ind = one_atom_group_vec[one_atom_group_vec_size-1];
		one_atom_group_vec.pop_back();
		
		for (i = multi_atgs_size-1; i >= 0; i--){
			vector<int> ith = multi_atgs[i];
			multi_atgs.pop_back();
			
			int ith_size = ith.size();
			vector<vector<int> > ith_arr;
			for (j = 0; j < ith_size; j++){
				const SIMPLE_ROAD* jroad = this->get_ij_simple_road(one_atom_ind, ith[j]);
				
				is_new_group = true;
				n = ith_arr.size();
				for (k = 0; k < n; k++){
					vector<int>& kth_atg = ith_arr[k];
					const SIMPLE_ROAD* kroad = this->get_ij_simple_road(one_atom_ind, kth_atg[0]);
					if (kroad->roadlen == jroad->roadlen){
						kth_atg.push_back(ith[j]);
						is_new_group = false;
						break;
					}
				}
				
				if (is_new_group){
					vector<int> atg;
					atg.push_back(ith[j]);
					ith_arr.push_back(atg);
				}
			}
			
			for (j = 0; j < ith_arr.size(); j++){
				vector<int> jth = ith_arr[j];
				if (1 == jth.size()){
					one_atom_group_vec.push_back(jth[0]);
					
					vector<int>* p_atg = new vector<int>();
					p_atg->push_back(jth[0]);
					atgs.push_back(p_atg);
				} else {
					buf_multi_atgs.push_back(jth);
				}
			}
		}
		
		for (i = buf_multi_atgs.size()-1; i >= 0; i--){
			vector<int> ith = buf_multi_atgs[i];
			buf_multi_atgs.pop_back();
			multi_atgs.push_back(ith);
		}
		
		one_atom_group_vec_size = one_atom_group_vec.size();
		multi_atgs_size = multi_atgs.size();
	}
	
	if (0 != multi_atgs_size){
		for (i = 0; i < multi_atgs_size; i++){
			vector<int>* p_atg = new vector<int>();
			for (j = 0; j < multi_atgs[i].size(); j++)
				p_atg->push_back(multi_atgs[i][j]);
			atgs.push_back(p_atg);			
		}
	}
	
	is_same_imp_mtx = CBaseFunc::new2DBoolArr(atnum, atnum);
	for (i = 0; i < atnum; i++)
		for (j = 0; j < atnum; j++)
			is_same_imp_mtx[i][j] = false;
	
	int atgs_size = atgs.size();
	for (i = 0; i < atgs_size; i++){
		vector<int>& ith = *atgs[i];
		int ith_size = ith.size();
		for (j = 0; j < ith_size; j++){
			int jind = ith[j];
			for (k = j+1; k < ith_size; k++){
				int kind = ith[j];
				is_same_imp_mtx[jind][kind] = is_same_imp_mtx[kind][jind] = true;
			}
		}
	}
}

LigAtomMatcher::LigAtomMatcher(Ligand* p_lig):lig(*p_lig){
	atnum = lig.size();
	
	double* vdwr = new double[atnum];
	AtomVarDerWaalRadius vdwrobj;
	for (int i = 0; i < atnum; i++)
		vdwr[i] = vdwrobj[p_lig->get_cared_atomsimpletype_in_lig(i)];

	double** adjmtx = CBaseFunc::new2Darr(atnum, atnum);	
	for (int i = 0; i < atnum; i++){
		for (int j = i+1; j < atnum; j++){
			bool is_connect = false;
			if (DONOTKNOW == p_lig->get_chemical_bond_type(i, j)) {
				double vdwij = (vdwr[i]>vdwr[j] ? vdwr[i] : vdwr[j])+0.06;
				double dis2 = CBaseFunc::distance2(lig[i], lig[j]);
				if (dis2 < vdwij*vdwij) is_connect = true;
			} else if (NOTCONNECTED != p_lig->get_chemical_bond_type(i, j))
				is_connect = true;

			if (is_connect)
				adjmtx[i][j] = adjmtx[j][i] = 0.5*(vdwr[i]+vdwr[j]);
		}
	}
	
	sr = new ShortestRoad(adjmtx, atnum);
	int*** all_roads = sr->getAllRoad8Floyd();
	int** all_road_lens = sr->getAllRoadLen8Floyd();
	
	for (int i = 0; i < atnum; i++)
		attypes_in_roads.push_back(extract_ith_roads(all_roads[i], all_road_lens[i]));
	
	// extract atom bonds, chemical bonds of neigbors
	for (int i = 0; i < atnum; i++){
		string at = p_lig->get_cared_atomsimpletype_in_lig(i); // atom type of ith atom
		vector<CHEMICAL_BOND_TYPE> cbts;  //interacted bond types in depth 1 
		vector<string> nats; // atom types of neighbors in depth 1
		for (int k = 0; k < atnum; k++){
			CHEMICAL_BOND_TYPE kcbt = p_lig->get_chemical_bond_type(i, k);
			if (NOTCONNECTED != kcbt){
				cbts.push_back(kcbt);
				nats.push_back(p_lig->get_cared_atomsimpletype_in_lig(k));
			}
		}
		
		ats.push_back(at);
		cbtss.push_back(cbts);
		natss.push_back(nats);
	}
	
	is_simple_same_imp_mtx = CBaseFunc::new2DBoolArr(atnum, atnum);
	for (int i = 0; i < atnum; i++){
		is_simple_same_imp_mtx[i][i] = true;
		for (int j = i+1; j < atnum; j++){
			is_simple_same_imp_mtx[i][j] = is_simple_same_imp_mtx[j][i] = this->is_simple_same_important(i, j);
		}
	}
	
	is_same_imp_mtx = CBaseFunc::new2DBoolArr(atnum, atnum);
	for (int i = 0; i < atnum; i++){
		vector<SIMPLE_ROAD* >& iroads = *attypes_in_roads[i];
		for (int j = i+1; j < atnum; j++){
			vector<SIMPLE_ROAD* >& jroads = *attypes_in_roads[j];
			if (is_simple_same_imp_mtx[i][j])
				is_same_imp_mtx[i][j] = is_same_imp_mtx[j][i] = is_same_roads(iroads, jroads);
		}
	}
	
	extract_atgs();
	
	togethor_mappings = NULL;
	delete[] vdwr;
	CBaseFunc::delete2Darr(adjmtx, atnum);
}

LigAtomMatcher:: ~LigAtomMatcher() {
	int n = atgs.size();
	for (int i = 0; i < n; i++){
		if (NULL != atgs[i])
			delete atgs[i];
	}
	if (NULL != togethor_mappings) CBaseFunc::delete2DBoolArr(n, togethor_mappings);
	
	n = attypes_in_roads.size();
	for (int i = 0; i < n; i++){
		vector<SIMPLE_ROAD* >& ith = *attypes_in_roads[i];
		if (NULL != attypes_in_roads[i]){
			int m = ith.size();
			for (int j = 0; j < m; j++){
				if (NULL != ith[j]){
					delete ith[j];
				}
			}
			delete attypes_in_roads[i];
		}
	}
	
	delete sr;
	CBaseFunc::delete2DBoolArr(atnum, is_simple_same_imp_mtx);
	CBaseFunc::delete2DBoolArr(atnum, is_same_imp_mtx);
}

inline bool LigAtomMatcher::is_same_roads(const vector<SIMPLE_ROAD* >& arvec, const vector<SIMPLE_ROAD* >& brvec) {
	int alen = arvec.size();
	int blen = brvec.size();
	if (alen == blen){
		double is_matched, ans = true;
		bool* is_used = CBaseFunc::new1Dbool(blen);
		for (int i = 0; i < alen; i++){
			SIMPLE_ROAD& ar = *arvec[i];
			is_matched = false;
			for (int j = 0; j < blen; j++) {
				if (is_used[j]) continue;
				
				SIMPLE_ROAD& br = *brvec[j];
				if (ar.roadlen==br.roadlen 
						&& this->is_simple_same_imp_mtx[ar.start_atind][br.start_atind]
						&& this->is_simple_same_imp_mtx[ar.end_atind][br.end_atind]){
					is_matched = true;
					is_used[j] = true;
					break;
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		
		delete[] is_used;
		return ans;
	}else return false;
}

inline vector<SIMPLE_ROAD* >* LigAtomMatcher::extract_ith_roads(int** ar, int *arl) {
	vector<SIMPLE_ROAD* >* arvec = new vector<SIMPLE_ROAD* >();
	for (int i = 0; i < atnum; i++){
		SIMPLE_ROAD* road = new SIMPLE_ROAD;
		
		road->roadlen = arl[i];
		int last_at_ind = 0;
		for (int k = 0; k < road->roadlen; k++) {
			if (-1 == ar[i][k]) break;
			last_at_ind = k;
		}
		road->start_atind = ar[i][0];
		road->end_atind = ar[i][last_at_ind];

		if (0 < road->roadlen){
			arvec->push_back(road);
		} else delete road;
	}
	
	if (0 >= arvec->size()){
		delete[] arvec;
		return NULL;
	}else{
		return arvec;
	}
}

inline const bool& LigAtomMatcher::is_same_important(const int& i, const int& j){
	return is_same_imp_mtx[i][j];
}

inline bool LigAtomMatcher::is_simple_same_important(const int& i, const int& j){
	string& iat = ats[i];
	string& jat = ats[j];
	if (iat != jat)
		return false;
		
	vector<CHEMICAL_BOND_TYPE>& icbts = this->cbtss[i];
	vector<CHEMICAL_BOND_TYPE>& jcbts = this->cbtss[j];
	
	int ilen = icbts.size();
	int jlen = jcbts.size();
	if (ilen != jlen)
		return false;
	
	vector<string>& inats = this->natss[i];
	vector<string>& jnats = this->natss[j];
	int in = inats.size();
	int jn = jnats.size();
	if (in != jn)
		return false;
		
	int k, l;
	bool is_matched, ans = true;
	{
		bool* is_used = CBaseFunc::new1Dbool(jlen);
		for (k = 0; k < ilen; k++){
			is_matched = false;
			for (l = 0; l < jlen; l++){
				if (is_used[l]) continue;
				if (icbts[k] == jcbts[l]) {
					is_matched = true;
					is_used[l] = true;
					break;
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		delete[] is_used; 
	}
	
	if (ans){
		bool* is_used = CBaseFunc::new1Dbool(jn);
		for (k = 0; k < in; k++){
			is_matched = false;
			for (l = 0; l < jn; l++){
				if (is_used[l]) continue;
				if (inats[k] == jnats[l]){
					is_matched = true;
					is_used[l] = true;
					break;						
				}
			}
			
			if (!is_matched){
				ans = false;
				break;
			}
		}
		delete[] is_used; 
	}
	
	return ans;
}

inline void CBaseFunc::print_help(const char* arg){
	cout << "DockEva is a method for evaluating lignad docking pose quality." << endl
	     << endl;
	cout << " Usage: " << arg << " structure_1.mol2 structure_2.mol2 [Options]" << endl << endl
		 << " Options:" << endl
		 << "   -t        Type of input ligand file format" << endl
		 << "               mol2 (default) : MOL2 format, see https://paulbourke.net/dataformats/mol2/" << endl
		 << "               sdf            : SDF format, see https://www.nonlinear.com/progenesis/sdf-studio/v0.9/faq/sdf-file-format-guidance.aspx" << endl
		 << "               pdb            : PDB format, see https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html" << endl
		 << "   -s        Score function for optimizing atom mapping" << endl
		 << "               rmsd (default) : Root mean square deviation" << endl
		 << "               lssco          : LS-score designed in LS-align" << endl
		 << "   -cbt      Do we need to load chemical bond types" << endl
		 << "               Y (default): Yes" << endl
		 << "               N          : No" << endl
		 << "   -maxrt   Set maximum running minutes for search reasonable atom mapping number" << endl 
		 << "               default: 3*24*60 minutes (3 days). " << endl
		 << "               e.g., \"-maxrt 3\", means taking 3 minutes at most to search reasonable atom mapping number." << endl
		 << "   -lh       Do we need to load 'H' atom" << endl
		 << "               Y          : Yes" << endl
		 << "               N (default): No" << endl
		 << "   -h        print this help" << endl << endl
		 << "   -v        print version" << endl << endl
		 << " Example usages:" << endl
		 << "    "<< arg <<" native_lig.mol2 decoy_lig.mol2" << endl
		 << "    "<< arg <<" native_lig.mol2 decoy_lig.mol2 -s lssco" << endl
		 << "    "<< arg <<" native_lig.mol2 decoy_lig.mol2 -t sdf" << endl
		 << "    "<< arg <<" native_lig.pdb decoy_lig.pdb -t pdb" << endl
		 << "    "<< arg <<" -h"<< endl << endl;
	exit(1);
}

inline void CBaseFunc::print_logo(){
	cout 
	<<"==================================================================" << endl
	<<"              ____             _    ___                           "<<endl
	<<"             (|   \\           | |  / (_)                         "<<endl
	<<"              |    | __   __  | |  \\__        __,                "<<endl
	<<"             _|    |/  \\_/    |/_) /    |  |_/  |                "<<endl
	<<"            (/\\___/ \\__/ \\___/| \\_/\\___/ \\/  \\_/|_/        "<<endl
	<<"                                                                  "<<endl
	<<"Version of DockEva: " << VERSION << endl
	<<"Please email comments and suggestions to Jun Hu (hj@ism.cams.cn) "<< endl
	<<"================================================================="<< endl << endl;
}

