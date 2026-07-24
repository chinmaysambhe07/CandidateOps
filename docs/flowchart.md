# CandidateOps Flowchart

```mermaid
flowchart TD
    %% Start
    Start([Start CandidateOps]) --> Init[Initialize Components]
    
    Init --> Auth{SAP Authentication\n(username, password)}
    Auth -- Failure --> AuthError[Authentication Error\nLog & Exit]
    Auth -- Success --> Setup[Setup Processing\nLoad Positions List]
    
    AuthError --> End([End])
    
    %% Main Processing Loop
    Setup --> LoopStart{Main Loop\n(Continuous or Single)}
    LoopStart -- Single Cycle --> ProcessPositions[Process Positions]
    LoopStart -- Continuous --> ProcessPositions
    
    ProcessPositions --> NextPosition{More Positions?}
    NextPosition -- Yes --> ProcessPosition[Process Single Position]
    NextPosition -- No --> CheckNewApps{Check for New Applications?}
    
    ProcessPosition --> Navigate[Navigate to Position\n(position_id)]
    Navigate --> GetPosDetails[Get Position Details]
    GetPosDetails --> GetCandidateIds[Get Candidate IDs for Position]
    
    GetCandidateIds --> NextCandidate{More Candidates?}
    NextCandidate -- Yes --> ProcessSingleCandidate[Process Single Candidate]
    NextCandidate -- No --> PositionComplete[Position Processing Complete]
    
    ProcessSingleCandidate --> CheckProcessedInSession{Already Processed\nin This Session?}
    CheckProcessedInSession -- Yes --> CandidateSkipped[Skip Candidate]
    CheckProcessedInSession -- No --> FetchDetails[Fetch Candidate Details\nfrom SAP]
    
    FetchDetails --> FindInExcel{Find Candidate\nin Excel Sheet}
    FindInExcel -- Not Found --> NewCandidate[Handle New Candidate]
    FindInExcel -- Found --> ExistingCandidate[Handle Existing Candidate]
    
    NewCandidate --> AddToExcel[Add to Excel Sheet]
    AddToExcel --> CreateFolder[Create Candidate Folder]
    CreateFolder --> DownloadAttachments[Download Attachments\n(resume, cover_letter, etc.)]
    DownloadAttachments --> SaveFiles[Save Files to Folder]
    SaveFiles --> UpdateStats[Update Statistics\n(+1 New, +Attachments)]
    UpdateStats --> CandidateProcessed[Candidate Processed]
    
    ExistingCandidate --> DataChanged{Has Data Changed?}
    DataChanged -- No --> CandidateSkipped2[Skip Candidate - No Changes]
    DataChanged -- Yes --> UpdateExcel[Update Excel Record]
    UpdateExcel --> DownloadMissing{Download Missing\nAttachments?}
    DownloadMissing -- Yes --> DownloadAttachs[Download Missing Attachments]
    DownloadAttachs --> SaveNewFiles[Save New Files]
    SaveNewFiles --> UpdateStats2[Update Statistics\n(+1 Updated, +New Attachments)]
    UpdateStats2 --> CandidateProcessed2[Candidate Processed]
    
    CandidateSkipped --> CandidateProcessed
    CandidateSkipped2 --> CandidateProcessed2
    CandidateProcessed --> CandidateProcessed2
    CandidateProcessed2 --> NextCandidate2{More Candidates?}
    NextCandidate2 -- Yes --> ProcessSingleCandidate
    NextCandidate2 -- No --> PositionComplete
    
    PositionComplete --> NextPosition
    
    %% New Applications Check (Continuous Mode Only)
    CheckNewApps --> HasNewApps{New Applications\nAvailable?}
    HasNewApps -- Yes --> IncrementCounter[Increment Cycle Counter]
    HasNewApps -- No --> IncrementCounter
    
    IncrementCounter --> WaitCycle[Wait for Check Interval\n(e.g., 300 seconds)]
    WaitCycle --> CheckShutdown{Shutdown Requested?\n(Ctrl+C or SIGTERM)}
    CheckShutdown -- No --> LoopStart
    CheckShutdown -- Yes --> Cleanup
    
    %% Single Cycle Path
    ProcessPositions --> CheckNewAppsSingle{Check for New Applications?\n(Optional in Single Mode)}
    CheckNewAppsSingle -- Yes --> HasNewAppsSingle{New Applications\nAvailable?}
    HasNewAppsSingle -- Yes --> IncrementCounterSingle[Increment Counter]
    HasNewAppsSingle -- No --> IncrementCounterSingle
    CheckNewAppsSingle -- No --> IncrementCounterSingle
    IncrementCounterSingle --> CheckShutdownSingle{Shutdown Requested?}
    CheckShutdownSingle -- No --> EndSingle[End Processing]
    CheckShutdownSingle -- Yes --> Cleanup
    
    %% Cleanup and End
    Cleanup --> CloseSAP[Close SAP Client Connection]
    CloseSAP --> FinalLog[Log Final Statistics]
    FinalLog --> End([End])
    
    %% Error Handling Subflow (simplified)
    classDef error fill:#FFEBEE,stroke:#C62828,stroke-width:2px;
    class AuthError error;
    
    %% Styling
    classDef startEnd fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px;
    classDef process fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F57F17,stroke-width:2px;
    classDef io fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;
    classDef cleanup fill:#FCE4EC,stroke:#880E4F,stroke-width:2px;
    
    class Start,End startEnd;
    class Init,Auth,Setup,ProcessPositions,ProcessPosition,NextPosition,GetPosDetails,GetCandidateIds,NextCandidate,ProcessSingleCandidate,CheckProcessedInSession,FetchDetails,FindInExcel,NewCandidate,ExistingCandidate,DataChanged,UpdateExcel,DownloadMissing,DownloadAttchs,SaveNewFiles,UpdateStats,UpdateStats2,CandidateProcessed,CandidateProcessed2,NextCandidate2,PositionComplete,CheckNewApps,HasNewApps,IncrementCounter,WaitCycle,CheckShutdown,Cleanup,CloseSAP,FinalLog process;
    class AuthError,CheckNewAppsSingle,HasNewAppsSingle,IncrementCounterSingle,CheckShutdownSingle,EndSingle decision;
    class CloseSAP,FinalLog cleanup;
```