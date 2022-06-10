
import sys,getopt
from datetime import datetime
from typing import Dict

from pandas import DataFrame

from emerge.analysis import Analysis
from emerge.analyzer import Analyzer
from emerge.config import *
from emerge.core import format_timedelta
from emerge.graph import GraphType
from emerge.stats import Statistics
from emerge.log import Logger, LogLevel
import coloredlogs


from emerge.languages.abstractparser import AbstractParser
from emerge.languages.javaparser import JavaParser
from emerge.languages.swiftparser import SwiftParser
from emerge.languages.cparser import CParser
from emerge.languages.cppparser import CPPParser
from emerge.languages.groovyparser import GroovyParser
from emerge.languages.javascriptparser import JavaScriptParser
from emerge.languages.typescriptparser import TypeScriptParser
from emerge.languages.kotlinparser import KotlinParser
from emerge.languages.objcparser import ObjCParser
from emerge.languages.rubyparser import RubyParser
from emerge.languages.pyparser import PythonParser

from calculate.tools import local_metrics_to_df

LOGGER = Logger(logging.getLogger('emerge'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)

PARSERS:Dict[str, AbstractParser] = {
    JavaParser.parser_name(): JavaParser(),
    SwiftParser.parser_name(): SwiftParser(),
    CParser.parser_name(): CParser(),
    CPPParser.parser_name(): CPPParser(),
    GroovyParser.parser_name(): GroovyParser(),
    JavaScriptParser.parser_name(): JavaScriptParser(),
    TypeScriptParser.parser_name(): TypeScriptParser(),
    KotlinParser.parser_name(): KotlinParser(),
    ObjCParser.parser_name(): ObjCParser(),
    RubyParser.parser_name(): RubyParser(),
    PythonParser.parser_name(): PythonParser()
}  
DEFAULT_CONFIG={
    "project_name": "example-project",
    "analysis_name": "check_files",
    "source_directory": None,
    # "only_permit_languages":['java'],
    "only_permit_file_extensions":[],
    "ignore_dependencies_containing":[],        
    "file_scan":[
        "number_of_methods",
        "source_lines_of_code",
        "dependency_graph",
        "louvain_modularity",
        "fan_in_out",
        "tfidf"],
    "entity_scan":[
        "number_of_methods",
        "source_lines_of_code",
        "dependency_graph",#(or dependency_graph/inheritance_graph/complete_graph)
        "louvain_modularity",
        "fan_in_out",
        "tfidf"
    ],
    "export":{
        "directory": None,
        "graphml":"",
        "dot":"",
        "d3":""
        # (and/or json/tabular_file/tabular_console_overall)
    }
} 
SUPPORT_LANG={
    "java":".java",
    "c":".c",
    "cpp":".cpp",
    "python":".py",
    "javascript":".js",
    "kotlin":".kt,.kts",
}
class GraphGenerator(Analyzer):
    
    def __init__(self,parsers=PARSERS):
        self._config=Configuration("test")
        self._parsers = parsers
        self._results = {}
        self.source_directory: str=""
        self.language:str=""
        self.output_directory="out"
        self.export_format:str=None
        self.project_name=None
        self.analysis_name="check_files"
        self.ignore_dependencies_containing:str=None
        self.file_scan=False
        self.entity_scan=False
        self.file_inheritance=False
        self.excludeExLib=False
    def main(self,argv):
        try:
            self.args_parse(argv)
        except:
            LOGGER.error("please check your arguments")
            return
        self.entry()
    def args_parse(self,argv):
        opts,args=getopt.getopt(argv,"s:o:l:p:a:",
            ["entity_scan","file_scan","file_inheritance","excludeExLib","format=","ignore_dependencies_containing="])
        for opts,arg in opts:
            if opts=="-s":
                self.source_directory = arg
            if opts=="-o":
                self.output_directory = arg
            if opts=="-l":
                self.language = arg
            if opts=="-p":
                self.project_name = arg
            if opts=="-a":
                self.analysis_name = arg
            if opts=="--entity_scan":
                self.entity_scan = True
            if opts=="--file_scan":
                self.file_scan = True
            if opts=="--file_inheritance":
                self.file_inheritance = True
            if opts=="--excludeExLib":
                self.excludeExLib = True
            if opts=="--format":
                self.export_format = arg
            if opts=="--ignore_dependencies_containing":
                self.ignore_dependencies_containing = arg
        if (self.project_name is None) or (self.language is None):
            print('!!!Usage: python generate.py -s source_directory -l language(s) [-o output_directory] \
                [-p project_name] [-a analysis_name] [--file_scan] [--entity_scan] [--file_inheritance] \
                [--excludeExLib] [--ignore_dependencies_containing=] [--format=graphml,dot,d3]')
            print("example:")
            print('python generate.py -s D:\idea_workspace\Analyser4J -l java -o out -p Analyser4J -a test --file_scan --entity_scan --file_inheritance --excludeExLib --format=graphml,d3,tabular_file')
            return
    def generate_metricDF(
        self,source_directory,language,project_name=None,analysis_name=None,
        ignore_dependencies_containing=None,export_format=None,output_directory=None
        ):
        config={
            "project_name": "example-project",
            "ignore_dependencies_containing":[],
            "only_permit_file_extensions":[],
            'file_scan':["number_of_methods","source_lines_of_code",
                "dependency_graph","louvain_modularity","fan_in_out","sna"],
            'entity_scan':["number_of_methods","source_lines_of_code",
                "dependency_graph","inheritance_graph","complete_graph",
                "louvain_modularity","fan_in_out"]
        }
        config['source_directory']=source_directory
        config['analysis_name']=analysis_name
        if project_name:
            config['project_name']=project_name
        else:
            config['project_name']="unamed"
        if ignore_dependencies_containing:
            config['ignore_dependencies_containing']=ignore_dependencies_containing.split(',')
        language=language.split(',')
        for k,v in SUPPORT_LANG.items():
            if k in language:
                config["only_permit_file_extensions"].extend(v.split(',')) 
        if export_format:
            config['export']={"directory": output_directory}
            export_format=export_format.split(',')
            for lformat in ConfigKeyExport:
                if lformat.name.lower() in export_format:
                    config['export'][lformat.name.lower()]=""
        analysis = Analysis()
        configAnalysis(analysis,config)
        analysis.start_timer()
        analysis=self.start_scanning(analysis,cal_metric=False)
        if self.file_inheritance: analysis.merge_file_inheritance()
        if analysis.contains_code_metrics:
                self._calculate_code_metric_results(analysis)
        if analysis.contains_graph_metrics:
            analysis.calculate_graph_representations()
            self._calculate_graph_metric_results(analysis)
            analysis.add_local_metric_results_to_graphs()
        local_metric_df=local_metrics_to_df(analysis.get_local_metric_results())        
        if output_directory:
            analysis.export()
        analysis.stop_timer()
        analysis.statistics.add(key=Statistics.Key.ANALYSIS_RUNTIME, value=analysis.duration())
        LOGGER.info_done(f'untime of analysis: {analysis.analysis_runtime}')
        self._clear_all_parsers()
        return local_metric_df

    def entry(self):
        config={
            "project_name": "example-project",
            "ignore_dependencies_containing":[],
            "only_permit_file_extensions":[],            
        }
        config['source_directory']=self.source_directory
        config['analysis_name']=self.analysis_name
        if self.project_name:
            config['project_name']=self.project_name
        else:
            config['project_name']="unamed"
        if self.ignore_dependencies_containing:
            config['ignore_dependencies_containing']=self.ignore_dependencies_containing.split(',')
        if self.export_format:
            config['export']={"directory": self.output_directory}
            export_format=self.export_format.split(',')
            for lformat in ConfigKeyExport:
                if lformat.name.lower() in export_format:
                    config['export'][lformat.name.lower()]=""

        language=self.language.split(',')
        for k,v in SUPPORT_LANG.items():
            if k in language:
                config["only_permit_file_extensions"].extend(v.split(','))               
        
        if self.file_scan:
            config['file_scan']=["number_of_methods","source_lines_of_code",
                "dependency_graph","louvain_modularity","fan_in_out","tfidf","sna"]
        if self.entity_scan:
            config['entity_scan']=["number_of_methods","source_lines_of_code",
                "dependency_graph","inheritance_graph","complete_graph",
                "louvain_modularity","fan_in_out","tfidf"]

        analysis = Analysis()
        configAnalysis(analysis,config)
        analysis.start_timer()
        start_time = datetime.now()
        analysis=self.start_scanning(analysis)
        if self.excludeExLib: analysis.clear_external()
        if self.file_inheritance: analysis.merge_file_inheritance()
        dur_time = format_timedelta(datetime.now()-start_time, '%H:%M:%S + %s ms')        
        analysis.export()
        analysis.stop_timer()
        
        LOGGER.info_done(f"finished in time: {dur_time}")
        analysis.statistics.add(key=Statistics.Key.ANALYSIS_RUNTIME, value=analysis.duration())
        self._clear_all_parsers()
        
    def start(self,**kwargs):
        analysis_dict=DEFAULT_CONFIG.copy()
        for k,v in kwargs.items():
            analysis_dict[k]=v
        if analysis_dict["source_directory"] is None:
            LOGGER.error("source_directory must be set")
            return
        only_permit_file_extensions:list = analysis_dict["only_permit_file_extensions"]
        if len(only_permit_file_extensions)==0:
            LOGGER.error("only_permit_file_extensions[] must be set")
            return
        self.start_with_config(analysis_dict)
        
    def start_with_config(self,analysis_dict:dict,doExport=True,file_inheritance=False,excludeExLib=False):
        analysis = Analysis()
        configAnalysis(analysis,analysis_dict)
        analysis.start_timer()
        self.start_scanning(analysis)

        if excludeExLib: analysis.clear_external()
        if file_inheritance: analysis.merge_file_inheritance()
        if doExport : analysis.export()
        
        

        analysis.stop_timer()
        analysis.statistics.add(key=Statistics.Key.ANALYSIS_RUNTIME, value=analysis.duration())
        self._clear_all_parsers()

    
    def start_scanning(self,analysis: Analysis,cal_metric=True):
        start_time = datetime.now()
        # 文件系统图
        self._create_filesystem_graph(analysis)
        if (ConfigKeyAnalysis.ENTITY_SCAN.name.lower() in analysis.scan_types) or \
            (ConfigKeyAnalysis.FILE_SCAN.name.lower() in analysis.scan_types):
            self._create_file_results(analysis)
            self._create_entity_results(analysis)
        LOGGER.info_done('scanning complete')
        if cal_metric:
            if analysis.contains_code_metrics:
                self._calculate_code_metric_results(analysis)
            if analysis.contains_graph_metrics:
                analysis.calculate_graph_representations()
                self._calculate_graph_metric_results(analysis)
                analysis.add_local_metric_results_to_graphs()
        stop_time = datetime.now()
        delta_total_runtime = stop_time - start_time
        analysis.total_runtime = format_timedelta(delta_total_runtime, '%H:%M:%S + %s ms')
        analysis.statistics.add(key=Statistics.Key.TOTAL_RUNTIME, value=analysis.total_runtime)
        # analysis.export()
        LOGGER.info_done(f'total runtime of analysis: {analysis.total_runtime}')
        return analysis




def configAnalysis(analysis: Analysis,analysis_dict:dict):
    print(analysis_dict)
    # check export config
    if ConfigKeyAnalysis.EXPORT.name.lower() in analysis_dict:
        export_config=analysis_dict[ConfigKeyAnalysis.EXPORT.name.lower()]
        #输出目录
        if ConfigKeyExport.DIRECTORY.name.lower() in export_config:
            export_directory = export_config[ConfigKeyExport.DIRECTORY.name.lower()]
            analysis.export_directory = export_directory
        #输出格式
        if ConfigKeyExport.GRAPHML.name.lower() in export_config:
            analysis.export_graphml = True
        if ConfigKeyExport.DOT.name.lower() in export_config:
            analysis.export_dot = True
        if ConfigKeyExport.TABULAR_FILE.name.lower() in export_config:
            analysis.export_tabular_file = True
        if ConfigKeyExport.TABULAR_CONSOLE_OVERALL.name.lower() in export_config:
            analysis.export_tabular_console_overall = True
        if ConfigKeyExport.TABULAR_CONSOLE.name.lower() in export_config:
            analysis.export_tabular_console = True
        if ConfigKeyExport.JSON.name.lower() in export_config:
            analysis.export_json = True
        if ConfigKeyExport.D3.name.lower() in export_config:
            analysis.export_d3 = True
        if ConfigKeyExport.FEATURE.name.lower() in export_config:
            analysis.export_feature = True

    # exclude directories and files from scanning
    if ConfigKeyAnalysis.IGNORE_DIRECTORIES_CONTAINING.name.lower() in analysis_dict:
        for directory in analysis_dict[ConfigKeyAnalysis.IGNORE_DIRECTORIES_CONTAINING.name.lower()]:
            analysis.ignore_directories_containing.append(directory)

    # ignore files if given in the configuration
    if ConfigKeyAnalysis.IGNORE_FILES_CONTAINING.name.lower() in analysis_dict:
        for file in analysis_dict[ConfigKeyAnalysis.IGNORE_FILES_CONTAINING.name.lower()]:
            analysis.ignore_files_containing.append(file)

    # ignore dependencies if given in the configuration
    if ConfigKeyAnalysis.IGNORE_DEPENDENCIES_CONTAINING.name.lower() in analysis_dict:
        for ignored_dependency in analysis_dict[ConfigKeyAnalysis.IGNORE_DEPENDENCIES_CONTAINING.name.lower()]:
            analysis.ignore_dependencies_containing.append(ignored_dependency)

    # add replace dependency substring mappings
    if ConfigKeyAnalysis.IMPORT_ALIASES.name.lower() in analysis_dict:
        for mapping in analysis_dict[ConfigKeyAnalysis.IMPORT_ALIASES.name.lower()]:
            for dependency_substring, replaced_dependency_substring in mapping.items():
                if analysis.import_aliases_available == False:
                    analysis.import_aliases_available = True
                analysis.import_aliases[dependency_substring] = replaced_dependency_substring

    # check if the analysis should only consider specified files
    if ConfigKeyAnalysis.ONLY_PERMIT_FILES_MATCHING_ABSOLUTE_PATH.name.lower() in analysis_dict:
        if type(analysis_dict[ConfigKeyAnalysis.ONLY_PERMIT_FILES_MATCHING_ABSOLUTE_PATH.name.lower()]) == list:
            for file in analysis_dict[ConfigKeyAnalysis.ONLY_PERMIT_FILES_MATCHING_ABSOLUTE_PATH.name.lower()]:
                if analysis.only_permit_files_matching_absolute_path_available == False:
                    analysis.only_permit_files_matching_absolute_path_available = True
                analysis.only_permit_files_matching_absolute_path.append(file)
        else:
            raise Exception(f'❗️{ConfigKeyAnalysis.ONLY_PERMIT_FILES_MATCHING_ABSOLUTE_PATH.name.lower()} '
                                f'must be a list of strings.')

    # load metrics from analysis
    if ConfigKeyAnalysis.FILE_SCAN.name.lower() in analysis_dict:
        # add all configured file_scan metrics
        for configured_metric in analysis_dict[ConfigKeyAnalysis.FILE_SCAN.name.lower()]:

            # necessary indicator what graph representations are relevant for graph based metrics
            if configured_metric == ConfigKeyFileScan.DEPENDENCY_GRAPH.name.lower():
                analysis.create_graph_representation(GraphType.FILE_RESULT_DEPENDENCY_GRAPH)

            # number of methods
            if configured_metric == ConfigKeyFileScan.NUMBER_OF_METHODS.name.lower():
                number_of_methods_metric = NumberOfMethodsMetric(analysis)
                LOGGER.debug(f'adding {number_of_methods_metric.pretty_metric_name}...')
                analysis.metrics_for_file_results.update({
                    number_of_methods_metric.metric_name: number_of_methods_metric
                })

            # source lines of code
            if configured_metric == ConfigKeyFileScan.SOURCE_LINES_OF_CODE.name.lower():
                source_lines_of_code_metric = SourceLinesOfCodeMetric(analysis)
                LOGGER.debug(f'adding {source_lines_of_code_metric.pretty_metric_name}...')
                analysis.metrics_for_file_results.update({
                    source_lines_of_code_metric.metric_name: source_lines_of_code_metric
                })

            # fan-in, fan-out
            if ConfigKeyFileScan.FAN_IN_OUT.name.lower() in configured_metric:
                LOGGER.debug(f'adding {FanInOutMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                fan_in_out_metric = FanInOutMetric(analysis, graph_representations)
                analysis.metrics_for_file_results.update({
                    fan_in_out_metric.metric_name: fan_in_out_metric
                })

            # louvain-modularity
            if ConfigKeyFileScan.LOUVAIN_MODULARITY.name.lower() in configured_metric:
                LOGGER.debug(f'adding {LouvainModularityMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                louvain_modularity_metric = LouvainModularityMetric(analysis, graph_representations)
                analysis.metrics_for_file_results.update({
                    louvain_modularity_metric.metric_name: louvain_modularity_metric
                })

            # tfidf
            if ConfigKeyFileScan.TFIDF.name.lower() in configured_metric:
                LOGGER.debug(f'adding {TFIDFMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                tfidf_metric = TFIDFMetric(analysis)
                analysis.metrics_for_file_results.update({
                    tfidf_metric.metric_name: tfidf_metric
                })
            
            # SNA
            if ConfigKeyFileScan.SNA.name.lower() in configured_metric:
                LOGGER.debug(f'adding {SocialNetworkMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                sna_metric = SocialNetworkMetric(analysis, graph_representations)
                analysis.metrics_for_file_results.update({
                    sna_metric.metric_name: sna_metric
                })
            # TODO: add more metrics

    if ConfigKeyAnalysis.ENTITY_SCAN.name.lower() in analysis_dict:
        for configured_metric in analysis_dict[ConfigKeyAnalysis.ENTITY_SCAN.name.lower()]:
            # necessary indicator what graph representations are relevant for graph based metrics
            if configured_metric == ConfigKeyEntityScan.DEPENDENCY_GRAPH.name.lower():
                analysis.create_graph_representation(GraphType.ENTITY_RESULT_DEPENDENCY_GRAPH)

            if configured_metric == ConfigKeyEntityScan.INHERITANCE_GRAPH.name.lower():
                analysis.create_graph_representation(GraphType.ENTITY_RESULT_INHERITANCE_GRAPH)

            # TODO: check if dependency/inheritance exist
            if configured_metric == ConfigKeyEntityScan.COMPLETE_GRAPH.name.lower():
                analysis.create_graph_representation(GraphType.ENTITY_RESULT_COMPLETE_GRAPH)

            # number of methods
            if configured_metric == ConfigKeyEntityScan.NUMBER_OF_METHODS.name.lower():
                LOGGER.debug(f'adding {NumberOfMethodsMetric.pretty_metric_name}...')
                number_of_methods_metric = NumberOfMethodsMetric(analysis)

                analysis.metrics_for_entity_results.update({
                    number_of_methods_metric.metric_name: number_of_methods_metric
                })

            # source lines of code
            if configured_metric == ConfigKeyEntityScan.SOURCE_LINES_OF_CODE.name.lower():
                LOGGER.debug(f'adding {SourceLinesOfCodeMetric.pretty_metric_name}...')
                source_lines_of_code_metric = SourceLinesOfCodeMetric(analysis)
                analysis.metrics_for_entity_results.update({
                    source_lines_of_code_metric.metric_name: source_lines_of_code_metric
                })

            # fan-in, fan-out
            if ConfigKeyEntityScan.FAN_IN_OUT.name.lower() in configured_metric:
                LOGGER.debug(f'adding {FanInOutMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                fan_in_out_metric = FanInOutMetric(analysis, graph_representations)

                analysis.metrics_for_entity_results.update({
                    fan_in_out_metric.metric_name: fan_in_out_metric
                })

            # louvain-modularity
            if ConfigKeyEntityScan.LOUVAIN_MODULARITY.name.lower() in configured_metric:
                LOGGER.debug(f'adding {LouvainModularityMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                louvain_modularity_metric = LouvainModularityMetric(analysis, graph_representations)

                analysis.metrics_for_entity_results.update({
                    louvain_modularity_metric.metric_name: louvain_modularity_metric
                })

                # tfidf
            if ConfigKeyEntityScan.TFIDF.name.lower() in configured_metric:
                LOGGER.debug(f'adding {TFIDFMetric.pretty_metric_name}...')
                graph_representations = analysis.existing_graph_representations
                tfidf_metric = TFIDFMetric(analysis)
                analysis.metrics_for_entity_results.update({
                    tfidf_metric.metric_name: tfidf_metric
                })

            # TODO: add more metrics

    if ConfigKeyAnalysis.FILE_SCAN.name.lower() in analysis_dict:
        analysis.scan_types.append(ConfigKeyAnalysis.FILE_SCAN.name.lower())

    if ConfigKeyAnalysis.ENTITY_SCAN.name.lower() in analysis_dict:
        analysis.scan_types.append(ConfigKeyAnalysis.ENTITY_SCAN.name.lower())

    analysis.analysis_name = analysis_dict[ConfigKeyAnalysis.ANALYSIS_NAME.name.lower()]
    analysis.project_name = analysis_dict[ConfigKeyAnalysis.PROJECT_NAME.name.lower()]
    analysis.source_directory = analysis_dict[ConfigKeyAnalysis.SOURCE_DIRECTORY.name.lower()]
    # TODO: check for other optional keys/values and assign

    if ConfigKeyAnalysis.ONLY_PERMIT_LANGUAGES.name.lower() in analysis_dict:
        analysis.only_permit_languages = analysis_dict[ConfigKeyAnalysis.ONLY_PERMIT_LANGUAGES.name.lower()]
    if ConfigKeyAnalysis.ONLY_PERMIT_FILE_EXTENSIONS.name.lower() in analysis_dict:
        analysis.only_permit_file_extensions = analysis_dict[ConfigKeyAnalysis.ONLY_PERMIT_FILE_EXTENSIONS.name.lower()]


if __name__ == '__main__':
    graphGenerator=GraphGenerator()
    sys.argv.pop(0)
    print(sys.argv)
    argv=sys.argv
    graphGenerator.main(argv)
    
    
