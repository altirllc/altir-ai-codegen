def log_data(chunk: dict, sections: list[str]):
    for section in sections:
        summary = chunk.get(section, {}).get("summary")
        if summary:
            print(summary)
            print("\n")

# src/utils/logger.py

import time
from typing import Dict, Any, List

class SimpleLogger:
    """Simple terminal logger matching your ASCII style"""
    
    def __init__(self):
        self.step_times = {}
        # Natural language descriptions for plan steps
        self.plan_descriptions = {
            "decode_files": "🔍 Looking at your message to understand what files you need",
            "fetch_files": "📥 Finding and reading the files from your project",
            "resolve_ambiguity": "🔍 Clarifying which files you meant",
            "analyse_feedback": "💬 Understanding your feedback",
            "llm_call": "🤖 Analyzing your files and planning the changes",
            "update_file": "✏️  Applying the requested changes to your files",
            "human_approval": "👤 Asking for your approval before proceeding",
            "approved_path": "✅ Processing your approval",
            "rejected_path": "❌ Processing your rejection"
        }
        
        # Plan workflow descriptions
        self.workflow_descriptions = {
            ('decode_files', 'fetch_files', 'llm_call', 'update_file', 'human_approval'): 
                "📝 File modification workflow (decode → fetch → analyze → update)",
            ('decode_files', 'fetch_files', 'llm_call'): 
                "📖 File analysis workflow (decode → fetch → analyze)",
            ('decode_files',): 
                "🔍 Basic file discovery workflow"
        }
    
    def log_step_start(self, step_name: str, details: str = ""):
        """Log the start of a step"""
        self.step_times[step_name] = time.time()
        
        # Create a clean step header
        print(f"\n┌─ 🔧 {step_name.upper().replace('_', ' ')}")
        if details:
            print(f"│  {details}")
        print("│")
    
    def log_step_info(self, message: str):
        """Log info within a step"""
        print(f"│  ℹ️  {message}")
    
    def get_task_description(self, task_name: str) -> str:
        """Get human-friendly description for a task"""
        return self.plan_descriptions.get(task_name, f"Working on {task_name.replace('_', ' ')}")
    
    def log_step_success(self, message: str):
        """Log success within a step"""
        print(f"│  ✅ {message}")
    
    def log_execution_plan(self, plan_steps: List[str]):
        """Log the execution plan in natural language"""
        print("│")
        print("│  📋 EXECUTION PLAN:")
        print("│")
        
        # Show workflow type
        plan_tuple = tuple(plan_steps)
        workflow_desc = self.workflow_descriptions.get(plan_tuple, "🔧 Custom workflow")
        print(f"│  {workflow_desc}")
        print("│")
        
        # Show individual steps
        print("│  📝 PLANNED STEPS:")
        for i, step in enumerate(plan_steps, 1):
            step_desc = self.plan_descriptions.get(step, f"🔧 {step.replace('_', ' ').title()}")
            print(f"│    {i}. {step_desc}")
        print("│")
    
    def log_task_execution_start(self, current_step: int, total_steps: int, task_name: str):
        """Log start of task execution with progress"""
        progress = f"Step {current_step + 1} of {total_steps}"
        task_desc = self.plan_descriptions.get(task_name, f"🔧 {task_name.replace('_', ' ').title()}")
        
        print(f"\n┌─ 🚀 WORKING ON {progress}")
        print(f"│  {task_desc}")
        print("│")
    
    def log_task_execution_error(self, error_msg: str):
        """Log task execution error"""
        print(f"│  ❌ Something went wrong: {error_msg}")
    
    def log_files_found(self, files_count: int):
        """Log how many files were found"""
        if files_count == 0:
            self.log_step_info("No files found in your request")
        elif files_count == 1:
            self.log_step_info("Found 1 file mentioned")
        else:
            self.log_step_info(f"Found {files_count} files mentioned")
    
    def log_ambiguous_files(self, ambiguous_count: int):
        """Log ambiguous files found"""
        if ambiguous_count == 1:
            self.log_step_info("⚠️  Found 1 file with unclear path")
        else:
            self.log_step_info(f"⚠️  Found {ambiguous_count} files with unclear paths")
        self.log_step_info("Will ask you to clarify which files you meant")
    
    def log_workflow_ending(self, reason: str):
        """Log when workflow is ending"""
        self.log_step_info(f"🏁 {reason}")
    
    def log_step_complete(self, step_name: str):
        """Log step completion"""
        if step_name in self.step_times:
            elapsed = time.time() - self.step_times[step_name]
            print(f"│  ✅ Done in {elapsed:.2f}s")
        else:
            print(f"│  ✅ Done")
        print("└" + "─" * 50)

# Global logger instance
logger = SimpleLogger()

# Enhanced log_data function (keep your existing one and add this)
def log_data(chunk: Dict[str, Any], sections: List[str]):
    """Your existing log_data function - keep as is for now"""
    # This will be enhanced later as you add more nodes
    pass