#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Unified interface for LLM providers using OpenAI format
# https://github.com/muxi-ai/onellm
#
# Copyright (C) 2025 Ran Aroussi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
# ============================================================================ #
# OneLLM EXAMPLE: Image Generation
# ============================================================================ #
#
# This example demonstrates how to use OneLLM to generate images from text
# prompts using AI image generation models like DALL-E.
# Key features demonstrated:
#
# - Text-to-image generation with descriptive prompts
# - Model selection and configuration
# - Image size and format options
# - Saving generated images to local filesystem
#
# CODEBASE RELATIONSHIP:
# ----------------------
# This example leverages OneLLM's support for:
# - Image generation API
# - Provider-specific image models
# - File handling and output management
# - Command-line argument processing
#
# RELATED EXAMPLES:
# ----------------
# - vision_example.py: Using images as input to LLMs
# - vision_capability_example.py: Testing vision capabilities with fallbacks
# - chat_completion_example.py: Text-based interactions with LLMs
#
# REQUIREMENTS:
# ------------
# - OneLLM
# - OpenAI API key with access to DALL-E models
# - Writeable file system for saving generated images
#
# EXPECTED OUTPUT:
# ---------------
# 1. Success message about the image generation
# 2. For DALL-E 3: The revised prompt that was used
# 3. The file path where the generated image was saved
# ============================================================================ #
"""

import os
import asyncio
import argparse

# Import the Image class from OneLLM
from onellm import Image


async def generate_image_example(prompt, model="dall-e-3", size="1024x1024", output_dir=None):
    """
    Generate an image from a text prompt and save it to a file.

    This function uses the OneLLM Image API to generate an image based on the provided
    text prompt using the specified DALL-E model. The generated image is saved to the
    specified output directory.

    Args:
        prompt (str): The text description of the image to generate
        model (str, optional): The DALL-E model to use. Defaults to "dall-e-3".
        size (str, optional): The dimensions of the generated image. Defaults to "1024x1024".
        output_dir (str, optional): Directory to save the generated image. If None, creates
                                   a "generated_images" directory in the current working directory.

    Returns:
        dict or None: The API response containing image data and file path if successful,
                     None if an error occurs.
    """
    try:
        # Generate a default output directory if not provided
        if not output_dir:
            output_dir = os.path.join(os.getcwd(), "generated_images")
            os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Print information about the generation request
        print(f"Generating image with prompt: '{prompt}'")
        print(f"Using model: {model}, size: {size}")

        # Generate the image using the OneLLM Image API
        # The model name is prefixed with "openai/" to specify the provider
        result = await Image.create(
            prompt=prompt,
            model=f"openai/{model}",
            size=size,
            output_dir=output_dir
        )

        # Print information about the generated image
        print("\nImage generated successfully!")

        # If the model is DALL-E 3, it provides a revised prompt that it used
        # to generate the image, which may differ from the original prompt
        if "revised_prompt" in result["data"][0]:
            print(f"\nRevised prompt: {result['data'][0]['revised_prompt']}")

        # Print the file path where the image was saved
        print(f"\nImage saved to: {result['data'][0]['filepath']}")

        return result
    except Exception as e:
        # Handle any errors that occur during image generation
        print(f"Error generating image: {e}")
        return None


def parse_arguments():
    """
    Parse command line arguments.

    This function sets up the argument parser for the script, defining the available
    command-line options and their default values.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate images with DALL-E using OneLLM")
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        default="A photorealistic image of a cute robot exploring a futuristic city",
        help="Text prompt describing the image to generate"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="dall-e-3",
        choices=["dall-e-3", "dall-e-2"],
        help="DALL-E model to use"
    )
    parser.add_argument(
        "--size", "-s",
        type=str,
        default="1024x1024",
        help="Size of the generated image (model-dependent)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Directory to save the generated image"
    )
    return parser.parse_args()


def main():
    """
    Run the image generation example.

    This function is the entry point of the script. It parses command-line arguments,
    checks for the required API key, and runs the image generation example.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Check if OpenAI API key is set in environment variables
    # This is required for authentication with the OpenAI API
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key: export OPENAI_API_KEY=your-api-key")
        return

    # Run the image generation example with the provided arguments
    # asyncio.run is used to run the async function in a synchronous context
    asyncio.run(generate_image_example(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        output_dir=args.output
    ))


if __name__ == "__main__":
    main()
