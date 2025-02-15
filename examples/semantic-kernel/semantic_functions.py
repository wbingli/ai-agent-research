#!/usr/bin/env python3
"""
Semantic Kernel Example demonstrating semantic functions and Microsoft service integration.
Shows how to use semantic functions for text processing with Azure OpenAI integration.
"""

import os
from typing import Optional
from dotenv import find_dotenv, load_dotenv
from termcolor import cprint

import semantic_kernel as sk
from semantic_kernel.connectors.ai import AzureOpenAIConnector
from semantic_kernel.memory import VolatileMemoryStore
from semantic_kernel.semantic_functions import PromptTemplate, PromptTemplateConfig

# Load environment variables
dotenv_path = find_dotenv()
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv()

class SemanticProcessor:
    """Handles text processing using semantic functions."""

    def __init__(self):
        """Initialize the semantic processor with Azure OpenAI."""
        # Initialize the kernel
        self.kernel = sk.Kernel()

        # Configure Azure OpenAI
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "text-davinci-003")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        # Add Azure OpenAI connector
        self.kernel.add_connector(
            AzureOpenAIConnector(
                deployment_name=deployment,
                endpoint=endpoint,
                api_key=api_key
            )
        )

        # Initialize memory
        memory_store = VolatileMemoryStore()
        self.kernel.register_memory_store(memory_store)

        # Import semantic functions
        self._import_semantic_functions()

    def _import_semantic_functions(self):
        """Import semantic functions from prompt templates."""
        # Import summarize skill
        self.summarize = self.kernel.import_semantic_skill_from_directory(
            "prompts", "summarize"
        )

        # Import analyze skill
        self.analyze = self.kernel.import_semantic_skill_from_directory(
            "prompts", "analyze"
        )

    async def process_text(
        self,
        text: str,
        analysis_focus: Optional[str] = None
    ) -> dict:
        """
        Process text using semantic functions.

        Args:
            text: The input text to process
            analysis_focus: Optional focus areas for analysis

        Returns:
            Dictionary containing summary and analysis
        """
        try:
            # Create context with input
            context = self.kernel.create_new_context()
            context["input"] = text

            if analysis_focus:
                context["focus"] = analysis_focus

            # Generate summary
            print("\nGenerating summary...")
            summary_result = await self.kernel.run_async(
                self.summarize["summarize"],
                input_context=context
            )

            # Generate analysis
            print("\nPerforming analysis...")
            analysis_result = await self.kernel.run_async(
                self.analyze["analyze"],
                input_context=context
            )

            return {
                "summary": str(summary_result),
                "analysis": str(analysis_result)
            }

        except Exception as e:
            print(f"\nError processing text: {str(e)}")
            raise

async def main():
    """Main function demonstrating semantic function usage."""
    # Initialize processor
    processor = SemanticProcessor()

    # Example text
    sample_text = """
    Artificial Intelligence (AI) is transforming how businesses operate and compete.
    Organizations are leveraging AI for automation, decision-making, and customer service.
    However, implementing AI systems requires careful planning, robust infrastructure,
    and consideration of ethical implications. Success with AI depends on having clear
    objectives, quality data, and the right expertise.
    """

    # Process text
    print("\nProcessing sample text...")
    try:
        results = await processor.process_text(
            sample_text,
            analysis_focus="business implications and technical requirements"
        )

        # Print results
        print("\nSummary:")
        print(results["summary"])

        print("\nAnalysis:")
        print(results["analysis"])

    except Exception as e:
        print(f"\nError in main: {str(e)}")
        raise

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
