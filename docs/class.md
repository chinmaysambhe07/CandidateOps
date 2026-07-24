# CandidateOps Class Diagram

```mermaid
classDiagram
    %% Core Classes
    class CandidateOpsOrchestrator {
        -sap_client: SAPClientInterface
excel_handler: ExcelHandler
file_manager: FileManager
_processed_candidates: Set[str]
_shutdown_requested: bool
+run_single_cycle(username: str, password: str, position_ids: List[str]) -> Dict
+run_continuous(username: str, password: str, position_ids: List[str], check_interval: int)
+stop()
+get_status() -> Dict
+_signal_handler(signum, frame)
+_process_position(position_id: str) -> Dict
+_process_candidate(candidate_id: str, position: Position) -> Dict
+_has_candidate_changed(existing: Candidate, updated: Candidate) -> bool
+_download_candidate_attachments(candidate: Candidate, existing: Candidate=None) -> Dict
+_check_for_new_applications() -> bool
    }
    
    %% Data Models
    class Candidate {
        candidate_id: str
        name: str
        email: str
        phone: str
        city: str
        current_position: str
        years_experience: int
        education: str
        skills: List[str]
        application_date: Optional[datetime]
        status: str
        resume_path: Optional[Path]
        cover_letter_path: Optional[Path]
        additional_attachments: List[Path]
        notes: str
        +__post_init__()
        +_validate()
        +_is_valid_email(email: str) -> bool
        +get_full_name() -> str
        +has_resume() -> bool
        +get_attachment_count() -> int
        +to_dict() -> Dict
        +from_dict(data: Dict) -> Candidate
    }
    
    class Position {
        position_id: str
        title: str
        department: str
        location: str
        description: str
        requirements: str
        url: str
        active: bool
        +__post_init__()
        +is_active() -> bool
        +get_display_name() -> str
    }
    
    class Application {
        application_id: str
        candidate: Candidate
        position: Position
        applied_at: datetime
        source: str
        cover_letter: str
        status: str
        +__post_init__()
        +is_recent(hours: int) -> bool
    }
    
    %% Service Interfaces
    class SAPClientInterface {
        <<interface>>
        +authenticate(username: str, password: str) -> bool
        +navigate_to_position(position_id: str) -> bool
        +get_position_details() -> Position
        +get_candidate_ids() -> List[str]
        +get_candidate_details(candidate_id: str) -> Candidate
        +download_candidate_attachment(candidate_id: str, attachment_type: str) -> Tuple[bytes, str]
        +is_new_application_available() -> bool
        +refresh_page() -> None
        +close() -> None
    }
    
    %% Service Implementations
    class BaseSAPClient {
        _authenticated: bool
        _current_position_id: Optional[str]
        +is_authenticated() -> bool
        +get_current_position_id() -> Optional[str]
        +_validate_authentication()
        +_validate_position_loaded()
    }
    
    class MockSAPClient {
        _demo_data: Dict
        _current_position: Optional[Position]
        _current_candidates: List[Candidate]
        +_generate_demo_data() -> Dict
        +authenticate(username: str, password: str) -> bool
        +navigate_to_position(position_id: str) -> bool
        +get_position_details() -> Position
        +get_candidate_ids() -> List[str]
        +get_candidate_details(candidate_id: str) -> Candidate
        +download_candidate_attachment(candidate_id: str, attachment_type: str) -> Tuple[bytes, str]
        +is_new_application_available() -> bool
        +refresh_page() -> None
        +close() -> None
    }
    
    %% Excel Service
    class ExcelHandler {
        template_path: Path
        output_path: Path
        sheet_name: str
        id_column: str
        workbook: Workbook
        worksheet: Worksheet
        +__init__(template_path: Path=None, output_path: Path=None)
        +_create_new_workbook() -> Workbook
        +read_candidates() -> List[Candidate]
        +write_candidates(candidates: List[Candidate]) -> None
        +_apply_excel_formatting() -> None
        +get_next_available_row() -> int
        +find_candidate_by_id(candidate_id: str) -> Optional[Candidate]
        +update_candidate(candidate: Candidate) -> bool
        +add_candidate(candidate: Candidate) -> None
    }
    
    %% File Service
    class FileManager {
        base_output_dir: Path
        attachments_dir_name: str
        max_filename_length: int
        +__init__(base_output_dir: Path=None)
        +create_candidate_folder(candidate: Candidate) -> Path
        +save_resume(candidate: Candidate, content: bytes, filename: str=None) -> Path
        +save_cover_letter(candidate: Candidate, content: bytes, filename: str=None) -> Path
        +save_attachment(candidate: Candidate, content: bytes, filename: str, attachment_type: str) -> Path
        +download_file_from_url(url: str, session_cookies: Dict=None, headers: Dict=None) -> bytes
        +get_candidate_folder_path(candidate: Candidate) -> Path
        +list_candidate_attachments(candidate: Candidate) -> List[Path]
        +clean_temp_files(max_age_hours: int) -> int
    }
    
    %% Utility Classes
    class LoggingSetup {
        +setup_logging(name: str=None) -> Logger
        +get_logger(name: str) -> Logger
    }
    
    class Helpers {
        +sanitize_filename(filename: str, max_length: int=255) -> str
        +generate_file_hash(file_path: Union[str, Path]) -> str
        +is_valid_email(email: str) -> bool
        +parse_date_string(date_str: str, formats: List[str]=None) -> Optional[datetime]
        +format_file_size(size_bytes: int) -> str
        +ensure_directory_exists(directory_path: Union[str, Path]) -> Path
        +chunk_list(items: List, chunk_size: int) -> List[List]
        +truncate_string(text: str, max_length: int, suffix: str="...") -> str
    }
    
    class Exceptions {
        <<abstract>> CandidateOpsException
        ConfigurationError
        AuthenticationError
        SAPConnectionError
        NavigationError
        DataExtractionError
        ElementNotFoundError
        TimeoutError
        ExcelError
        FileOperationError
        ValidationError
        MonitoringError
    }
    
    %% Configuration
    class Settings {
        app_name: str
        version: str
        debug: bool
        database: DatabaseSettings
        sap: SapSettings
        excel: ExcelSettings
        file: FileSettings
        logging: LoggingSettings
        monitoring: MonitoringSettings
    }
    
    %% Relationships
    CandidateOpsOrchestrator "1" -- "1" SAPClientInterface : uses
    CandidateOpsOrchestrator "1" -- "1" ExcelHandler : uses
    CandidateOpsOrchestrator "1" -- "1" FileManager : uses
    
    SAPClientInterface <|.. BaseSAPClient : implements
    BaseSAPClient <|-- MockSAPClient : extends
    
    CandidateOpsOrchestrator "1" -- "0..*" Candidate : processes
    CandidateOpsOrchestrator "1" -- "0..*" Position : processes
    
    Settings --> DatabaseSettings : contains
    Settings --> SapSettings : contains
    Settings --> ExcelSettings : contains
    Settings --> FileSettings : contains
    Settings --> LoggingSettings : contains
    Settings --> MonitoringSettings : contains
    
    %% Dependencies
    Candidate ..> LoggingSetup : uses
    Position ..> LoggingSetup : uses
    Application ..> LoggingSetup : uses
    SAPClientInterface ..> LoggingSetup : uses
    BaseSAPClient ..> LoggingSetup : uses
    MockSAPClient ..> LoggingSetup : uses
    ExcelHandler ..> LoggingSetup : uses
    FileManager ..> LoggingSetup : uses
    Helpers ..> LoggingSetup : uses
    
    CandidateOpsOrchestrator ..> Settings : uses
    ExcelHandler ..> Settings : uses
    FileManager ..> Settings : uses
    MockSAPClient ..> Settings : uses
    
    %% Styling
    classDef orchestrator fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef model fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef service fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px;
    classDef utility fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    classDef exception fill:#FFEBEE,stroke:#C62828,stroke-width:2px;
    classDef config fill:#FCE4EC,stroke:#880E4F,stroke-width:2px;
    
    class CandidateOpsOrchestrator orchestrator;
    class Candidate,Position,Application model;
    class SAPClientInterface,BaseSAPClient,MockSapClient,ExcelHandler,FileManager service;
    class LoggingSetup,Helpers utility;
    class Exceptions exception;
    class Settings config;
```