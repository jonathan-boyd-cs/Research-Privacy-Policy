# Research Through Python Networking
## Can Informative Web Scrapers Be Built to Analyze Text Such as Privacy Policies?

### A University of Iowa Research Project : Networking 3640

#### Please see the requirements.txt file for information on necessary packages if you wish to explore the codebase.

The question arose... How does a computer scientist develop a methodology to research privacy policy practices as they stand today? This question was resolved to an effort to develop a comprehensive and generalized web scraper, in order to analyze various website's privacy policy pages. The motive; to find key words and phrases and develop a meaningful scoring system or understanding with this newfound information. The details of this pursuit are found in the <code>'Research-Policy.pdf'</code> document.
<br>

### Direction
The codebase is extensive and requires time to develop a sound understanding. With time, it becomes clear that the entirety of the system's <code>(WAS: Web Analysis Suite)</code> function is non-specialized, and is very much usable for different tasks. Various components are still under-developed. Bugs corresponding to the error handling are still being addressed, as the project is still being worked on for curiousity sake.
<br>

#### The easiest way to get the ball rolling...
The program provides a simplified interface to mask the complexity of operation.
Navigating into the <code>WebScraperModule</code>, one finds the <code>WebAnalysisSuite</code>. This class can be used in tangent with the <code>DataStorageModule.WebScraperStorageModule.WASManager (WASM)</code> in order to produce a simple and efficient result. __It is recommended to observe the example implementation__ of the <code>WAS</code> in the <code>crawler</code> folder, within the policy scrape demonstration. The WASM can be observed functioning properly in the 0 file of the <code>analysis</code> folder.
<br>

The <code>WAS</code> handles the creation of folders if a non-existent directory is specified. __It is recommended, if not essential__, to utilize relative paths. No other method has been tested or attempted. The segment is reasonably documented to provide guidance on the parameters of the constructor. The <code>headless</code> and <code>slow_mo</code> options correspond to the mode of the underlying Playwright driver.
<br>

The most important consideration is the structure of the keyword dictionaries and website dictionaries passed to these objects. Please see the website gathering <code>Runs_Cumulative</code> and the <code>PolicyQueryModule</code> for examples of the functionality of the program. The <code>WAS</code> and its data cleaning pipeline (Mediated by the <code>WASM</code>) are designed to operate on variable data. It is only essential to understand the structures provided to these objects. Specifying a heirarchial depth to the <code>WASM</code> that is not characteristic of the phrase dictionary tree may yield unknown results... It is also essential to understand the supposed column names for the website dictionary tree. The <code>WAS</code> cleaning pipeline will handle attributing column titles to the node data. Again, the aforementioned example files give a clear example of what is possible. The example output files are mixed with testing data. Various files illustrate the effect of manually switching from one page to another. This is detailed in the research paper. The <code>WAS</code> is best operated with a user in front of the screen... (better for the job market right?). This is due to an issue where certain websites coerce the WAS Playwright driver to open privacy policies on a new page. Logic has not yet been implemented to account for this. If not caught, the WAS will parse the home page and ignore the policy page. This occurance is variable. The bulk of observed output files, beyond those hampered by web security, clearly detail policy information having been parsed.

### PLEASE OBSERVE THE REQUIREMENTS.TXT DOCUMENT FOR NECESSARY INSTALLS
### THIS APPLICATION WAS DEVELOPED WITH THE LATEST VERSION OF PYTHON3

There are no special command-line arguments required for this codebase to operate. It will be proven highly useful and straightforward with time spent exploring each module.

Interesting results and follow up planning is detailed in the research paper connected to this repository.


