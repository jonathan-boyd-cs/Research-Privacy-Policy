import sys
sys.path.append('../')
from FileManager.file_manager import FileManager
from DataStorageModule.GraphicalStorageModule.dataframe_store import CSVToDataFrameStore
from StatisticalModule.DataPreprocessorModule.preprocessor import DataPreprocessor
import pandas as pd

name = 'post-scrape-preprocess'
out_directory_CSVs = './PostScrapeProcessing/CSVs/'
log_directory = './PostScrapeProcessing/Logs/'
verbose = True


csv_file_main = './PostScrapeClean/post-scrape-results-2.csv'

file_manager = FileManager(name,log_directory,verbose)
CSV_DFS = CSVToDataFrameStore(name, out_directory_CSVs,log_directory,verbose)

main_csv_name = 'main'
variation_1_on_main = 'clean_main_1'
variation_2_on_main = 'clean_main_traffic_value_and_rating'
variation_3_on_main = 'clean_main_complexity_scores'
variation_4_on_main = 'clean_main_composition_length'
variation_5_on_main = 'clean_main_word_forms'
variation_6_on_main = 'clean_main_dnsmi'
variation_7_on_main = 'clean_main_avg_complexity'
variation_8_on_main = 'clean_main_value-to-avg'




def main():
    CSV_DFS.load_and_store(main_csv_name, csv_file_main)
    main_frame = CSV_DFS.get(main_csv_name)
    
    # variation 1
    exclusions_cols = [7,8] # Country , State -> excess to pre-existing
    exclusions_rows = [54] # removing a false input --> says 'statefarm' is the state
    cols = [ x for x in range(len(main_frame[0])) if x not in exclusions_cols]
    CSV_DFS.generate_variation(main_csv_name,variation_1_on_main, cols, exclusions_rows)
    CSV_DFS.to_csv(variation_1_on_main)
    
    # TRAFFIC VALUATION AND DOMAIN RATING
    cols = [3,0,1,2,4,5,6]
    exclusions_rows_null = []
    CSV_DFS.generate_variation(variation_1_on_main, variation_2_on_main,
                               cols, exclusions_rows_null)
    CSV_DFS.to_csv(variation_2_on_main)
    
    # COMPLEXITY
    cols = [3,0,1,2,7,8,9,10,11,12,17,18]
    CSV_DFS.generate_variation(variation_1_on_main, variation_3_on_main,
                               cols, exclusions_rows_null)
    CSV_DFS.to_csv(variation_3_on_main)
    
    # COMPOSITION AND LENGTH
    cols = [3,0,1,2,12,14,15,16,19]
    CSV_DFS.generate_variation(variation_1_on_main, variation_4_on_main,
                               cols, exclusions_rows_null)
    CSV_DFS.to_csv(variation_4_on_main)
    
    #WORD FORMS
    cols = [3,0,1,2,20,21,22,23,24,25,26,27,28]
    CSV_DFS.generate_variation(variation_1_on_main, variation_5_on_main,
                               cols, exclusions_rows_null)
    CSV_DFS.to_csv(variation_5_on_main)
    
    
    # DNSMI
    cols = [3,0,1,2,29]
    exceptions = {
        29:["N/A"] 
    }
    CSV_DFS.generate_variation(variation_1_on_main, variation_6_on_main,
                               cols, exclusions_rows_null,exceptions)
    CSV_DFS.to_csv(variation_6_on_main)
    
    


    df = CSV_DFS.to_pandas(variation_3_on_main)
    #print(df)
    df.iloc[:,4] = pd.to_numeric(
        df.iloc[:,4], errors='coerce')
    df.iloc[:,5] = pd.to_numeric(
        df.iloc[:,5], errors='coerce')
    df.iloc[:,6] = pd.to_numeric(
        df.iloc[:,6], errors='coerce')
    df.iloc[:,7] = pd.to_numeric(
        df.iloc[:,7], errors='coerce')
    df.iloc[:,8] = pd.to_numeric(
        df.iloc[:,8], errors='coerce')
    df.iloc[:,9] = pd.to_numeric(
        df.iloc[:,9], errors='coerce')
    df.iloc[:,10] = pd.to_numeric(
        df.iloc[:,10], errors='coerce')
    df.iloc[:,11] = pd.to_numeric(
        df.iloc[:,11], errors='coerce')
    df['Complexity Avg'] = (df.iloc[:,4:11].mean(axis=1))

    file = out_directory_CSVs+"clean_main_avg_complex.csv"
    df.to_csv(file)
    CSV_DFS.store(variation_7_on_main,df)
    
    
    # ONLY VALUES TO AVG
    cols = [3,4,5,6]
    CSV_DFS.generate_variation(variation_1_on_main, variation_8_on_main,
                               cols, exclusions_rows_null)
    d = CSV_DFS.to_pandas(variation_8_on_main)
    d['Complexity Avg'] = df['Complexity Avg']
    CSV_DFS.store(variation_8_on_main,d)
    
    file = out_directory_CSVs+"clean_main_values_to_complex.csv"
    d.to_csv(file)
    
    
    
if __name__ == '__main__':
    main()
    