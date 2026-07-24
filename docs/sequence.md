# CandidateOps Sequence Diagram

```mermaid
sequenceDiagram
    participant User as User/Operator
    participant CLI as CLI Interface
    participant Orch as CandidateOps Orchestrator
    participant SAP as SAP Client
    participant Excel as Excel Handler
    participant File as File Manager
    participant DB as Excel Tracking Sheet
    participant FS as File System
    
    %% Initialize
    User->>CLI: Run with credentials
    CLI->>Orch: initialize()
    Orch->>SAP: create_sap_client()
    Orch->>Excel: create_excel_handler()
    Orch->>File: create_file_manager()
    
    %% Main Processing Loop
    loop Continuous Monitoring (if enabled)
        User->>Orch: run_continuous(username, password)
        
        %% Authentication
        Orch->>SAP: authenticate(username, password)
        alt Success
            SAP-->>Orch: True (authenticated)
        else Failure
            SAP-->>Orch: AuthenticationError
            Orch-->>User: Error: Authentication failed
            break
        end
        
        %% Process Positions
        loop For each position
            Orch->>SAP: navigate_to_position(position_id)
            SAP-->>Orch: True (navigated)
            
            Orch->>SAP: get_position_details()
            SAP-->>Orch: Position object
            
            Orch->>SAP: get_candidate_ids()
            SAP-->>Orch: List of candidate IDs
            
            loop For each candidate ID
                Orch->>SAP: get_candidate_details(candidate_id)
                SAP-->>Orch: Candidate object
                
                opt New candidate (not in Excel)
                    Orch->>Excel: find_candidate_by_id(candidate_id)
                    Excel-->>Orch: None
                    
                    Orch->>Excel: add_candidate(candidate)
                    Excel->>DB: INSERT new record
                    Orch->>File: create_candidate_folder(candidate)
                    File->>FS: Create folder structure
                    
                    opt Download attachments
                        Orch->>SAP: download_candidate_attachment(candidate_id, "resume")
                        SAP-->>Orch: (content, filename)
                        Orch->>File: save_resume(candidate, content, filename)
                        File->>FS: Save resume file
                        
                        Orch->>SAP: download_candidate_attachment(candidate_id, "cover_letter")
                        SAP-->>Orch: (content, filename)
                        Orch->>File: save_cover_letter(candidate, content, filename)
                        File->>FS: Save cover letter file
                    end
                    
                else Existing candidate (in Excel)
                    Orch->>Excel: find_candidate_by_id(candidate_id)
                    Excel-->>Orch: Existing Candidate
                    
                    opt Candidate data changed
                        Orch->>Excel: update_candidate(candidate)
                        Excel->>DB: UPDATE existing record
                        
                        opt Download missing attachments
                            Orch->>SAP: download_candidate_attachment(candidate_id, "resume")
                            SAP-->>Orch: (content, filename)
                            opt File doesn't exist
                                Orch->>File: save_resume(candidate, content, filename)
                                File->>FS: Save resume file
                            end
                            
                            Orch->>SAP: download_candidate_attachment(candidate_id, "cover_letter")
                            SAP-->>Orch: (content, filename)
                            opt File doesn't exist
                                Orch->>File: save_cover_letter(candidate, content, filename)
                                File->>FS: Save cover letter file
                            end
                        end
                    end
                end
            end
            
            Orch->>SAP: is_new_application_available()
            SAP-->>Orch: Boolean (new apps available)
            
            Orch->>SAP: refresh_page()
            SAP-->>Orch: Success
        end
        
        %% Wait for next cycle
        Orch->>Orch: sleep(check_interval)
    end
    
    %% Shutdown
    User->>Orch: Ctrl+C or SIGTERM
    Orch->>SAP: close()
    SAP-->>Orch: Resources released
    Orch-->>User: Application terminated gracefully
    
    %% Styling Notes
    %% Success paths are solid lines
    %% Error paths would be dashed with red color in actual diagram
```