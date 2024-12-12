import sys
sys.path.append('../')
from FileManager.file_manager import FileManager
from DataStorageModule.GraphicalStorageModule.dataframe_store import CSVToDataFrameStore
from StatisticalModule.DataPreprocessorModule.preprocessor import DataPreprocessor
from StatisticalModule.RegressionModule.regression_engine import RegressionEngine
from StatisticalModule.ClusterModule.cluster_engine import ClusterEngine
from ErrorHandleModule.general import time_stamped_msg 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


name = 'bar-pie-graphing-exploration'
out_directory_Graphs = './Graphing/Bars-Plots/'
log_directory = './Logs/'
verbose = True


main_csv_name = 'main'
variation_1_on_main = 'clean_main_1'
variation_2_on_main = 'clean_main_traffic_value_and_rating'
variation_3_on_main = 'clean_main_complexity_scores'
variation_4_on_main = 'clean_main_composition_length'
variation_5_on_main = 'clean_main_word_forms'
variation_6_on_main = 'clean_main_dnsmi'
variation_7_on_main = 'clean_main_avg_complexity'
variation_8_on_main = 'clean_main_value_to_complex'

csv_files = {
             variation_1_on_main:'./PostScrapeProcessing/CSVs/clean_main_1.csv',
             variation_2_on_main:'./PostScrapeProcessing/CSVs/clean_main_traffic_value_and_rating.csv',
             variation_3_on_main:'./PostScrapeProcessing/CSVs/clean_main_complexity_scores.csv',
             variation_4_on_main:'./PostScrapeProcessing/CSVs/clean_main_composition_length.csv',
             variation_5_on_main:'./PostScrapeProcessing/CSVs/clean_main_word_forms.csv',
             variation_6_on_main:'./PostScrapeProcessing/CSVs/clean_main_dnsmi.csv'
            ,variation_7_on_main:'./PostScrapeProcessing/CSVs/clean_main_avg_complex.csv',
             variation_8_on_main:'./PostScrapeProcessing/CSVs/clean_main_values_to_complex.csv',

             }

file_manager = FileManager(name,log_directory,verbose)
CSV_DFS = CSVToDataFrameStore(name, out_directory_Graphs,log_directory,verbose)
DP = DataPreprocessor()

for variation in csv_files:
    CSV_DFS.load_and_store(variation, csv_files[variation])
    
# LOAD PANDAS
var1 = CSV_DFS.to_pandas(variation_1_on_main)
var2 = CSV_DFS.to_pandas(variation_2_on_main)
var3 = CSV_DFS.to_pandas(variation_3_on_main)
var4 = CSV_DFS.to_pandas(variation_4_on_main)
var5 = CSV_DFS.to_pandas(variation_5_on_main)
var6 = CSV_DFS.to_pandas(variation_6_on_main)
var7 = CSV_DFS.to_pandas(variation_7_on_main)
var8 = CSV_DFS.to_pandas(variation_8_on_main)

var1.fillna(False)
var1 = DP.encode_binary(var1,var1.shape[1]-2)

def generate_bars(x_constraint, out_directory_Graphs):
    out_directory_Graphs = "{}{}".format(out_directory_Graphs, "{}/".format(x_constraint))
    file_manager.assure_directory(out_directory_Graphs)
    
    title =f"Traffic Value by {x_constraint}(sum)"
    xlabel=x_constraint
    ylabel="traffic-value"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].sum().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()
    title =f"Traffic Value by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="traffic-value"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()


    title =f"Domain Rating by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="domain-rating"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()
    title =f"Policy flesch_kincaid by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="flesch_kincaid"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    plt.clf()
    title =f"Policy Coleman Liau by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="flesch_kincaid"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Automated Readability Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="automated_readability"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()


    title =f"Policy Gunning Fog Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="gunning_fog"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Smog Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="smog"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Sentence Count Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="sentence_count"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()


    title =f"Policy Long Word Count Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="long_word_count"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Reading Time by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="reading_time"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Standard Readability Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="standard"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Dale Chall Score by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="dale_chall"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy Average Sentence Length by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="avg_sentence_length"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy WORD-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="WORDS"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy CAPABILITY-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="CAPABILITY"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy LEGAL-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="LEGAL"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy BUSINESS_FOCUS-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="BUSINESS_FOCUS"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy UTILIZATION-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="UTILIZATION"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy INNOVATION-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="INNOVATION"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy SECURITY-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="SECURITY"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()


    title =f"Policy EDUCATION-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="EDUCATION"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy TECHNOLOGY-key by {x_constraint}(mean)"
    xlabel=x_constraint
    ylabel="TECHNOLOGY"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].mean().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    title =f"Policy DNSMI by {x_constraint}(sum)"
    xlabel=x_constraint
    ylabel="DNSMI"
    var1[ylabel] = pd.to_numeric(var1[ylabel])
    var1.groupby(xlabel)[ylabel].sum().plot.bar(x=xlabel,y=ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale()
    plt.tight_layout()
    m = time_stamped_msg('{}-{}'.format('bars',title))
    plt.savefig(
        fname="{}{}.pdf".format(out_directory_Graphs,m),
        orientation='landscape',
        format='pdf',
    )

    plt.clf()

    
generate_bars('Industry',out_directory_Graphs)
generate_bars('Country',out_directory_Graphs)
generate_bars('State',out_directory_Graphs)
generate_bars('DNSMI',out_directory_Graphs)