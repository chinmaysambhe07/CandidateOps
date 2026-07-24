# CandidateOps Architecture Diagram

```mermaid
graph TD
    %% Main Components
    subgraph Application Layer
        CLI[Command Line Interface] --> Orchestrator[CandidateOps Orchestrator]
    end
    
    subgraph Business Logic
        Orchestrator --> PositionProcessor[Position Processor]
        Orchestrator --> CandidateProcessor[Candidate Processor]
        Orchestrator --> AttachmentManager[Attachment Manager]
        Orchestrator --> ExcelManager[Excel Manager]
        Orchestrator --> FileManager[File Manager]
        Orchestrator --> SAPClient[SAP Client Interface]
    end
    
    subgraph Service Layer
        SAPClient --> |Real Implementation| RealSAPClient[Real SAP Client<br/>(Selenium/Web Scraping)]
        SAPClient --> |Mock Implementation| MockSAPClient[Mock SAP Client<br/>(For Demo/Testing)]
        ExcelManager --> ExcelHandler[Excel Handler<br/>(pandas/openpyxl)]
        FileManager --> FileManagerImpl[File Manager<br/>(File System Operations)]
    end
    
    subgraph Data Layer
        ExcelHandler --> ExcelFile[(Excel Tracking Sheet)]
        FileManagerImpl --> CandidateFolders[(Candidate Data Folders)]
        ExcelFile --> |Reads/Writes| CandidateData[Candidate Records]
        CandidateFolders --> |Contains| Resume[Resume Files]
        CandidateFolders --> |Contains| CoverLetter[Cover Letter Files]
        CandidateFolders --> |Contains| Attachments[Other Attachments]
    end
    
    subgraph External Systems
        RealSAPClient --> |HTTP/SAP RFC| SAPPortal[SAP Career Portal]
        SAPPortal --> |Returns| PositionData[Position Information]
        SAPPortal --> |Returns| CandidateDataRaw[Candidate Data]
        SAPPortal --> |Provides| Attachments[Attachment Files]
    end
    
    %% Data Flow
    Orchestrator --> |1. Authenticate| SAPClient
    Orchestrator --> |2. Navigate to Position| SAPClient
    Orchestrator --> |3. Get Position Details| SAPClient
    Orchestrator --> |4. Get Candidate IDs| SAPClient
    Orchestrator --> |5. Process Each Candidate| SAPClient
    SAPClient --> |6. Get Candidate Details| SAPClient
    SAPClient --> |7. Download Attachments| SAPClient
    Orchestrator --> |8. Update Candidate| ExcelManager
    Orchestrator --> |9. Save Files| FileManager
    Orchestrator --> |10. Check for New Apps| SAPClient
    
    %% Styling
    classDef application fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef business fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef service fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px;
    classDef data fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    classDef external fill:#FFEBEE,stroke:#C62828,stroke-width:2px;
    
    class CLI,Orchestrator application;
    class PositionProcessor,CandidateProcessor,AttachmentManager,ExcelManager,FileManager,SAPClient business;
    class RealSAPClient,MockSAPClient,ExcelHandler,FileManagerImpl service;
    class ExcelFile,CandidateFolders,Resume,CoverLetter,Attachments,CandidateData data;
    class SAPPortal,PositionData,CandidateDataRaw,Attachments external;
```
```