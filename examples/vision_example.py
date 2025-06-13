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
# OneLLM EXAMPLE: Vision Model Usage
# ============================================================================ #
#
# This example demonstrates how to use OneLLM to analyze images using
# vision-capable LLMs and have multi-turn conversations about visual content.
# Key features demonstrated:
#
# - Sending images to vision-capable LLMs
# - Creating multi-modal messages with text and images
# - Conducting multi-turn conversations about images
# - Configuring vision model parameters
#
# CODEBASE RELATIONSHIP:
# ----------------------
# This example leverages OneLLM's support for:
# - ChatCompletion API with multi-modal inputs
# - Provider-specific vision models
# - Image URL handling and message formatting
# - Token tracking and usage monitoring
#
# RELATED EXAMPLES:
# ----------------
# - vision_capability_example.py: Testing model vision capabilities with fallbacks
# - chat_completion_example.py: Text-only model interactions
# - image_generation_example.py: Creating images (inverse operation)
#
# REQUIREMENTS:
# ------------
# - OneLLM
# - OpenAI API key with access to vision-capable models
#
# EXPECTED OUTPUT:
# ---------------
# 1. Initial model response describing the contents of the provided image
# 2. Follow-up response to a question about the image (showing context retention)
# 3. Token usage information for the API calls
# ============================================================================ #
"""

import os
from typing import List, Dict, Any

from onellm import ChatCompletion
from onellm.config import set_api_key


def create_message_with_image(image_url: str) -> List[Dict[str, Any]]:
    """
    Create a message that includes both text and an image.

    This function constructs a conversation message list that contains a system
    message defining the assistant's role and a user message with both text and
    image content. The image is referenced by URL.

    Args:
        image_url: URL of the image to process

    Returns:
        List of messages for the conversation, formatted for vision-capable models
    """
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that can see and understand images."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image? Please describe it in detail."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                        "detail": "high"  # Options: auto, low, high
                    }
                }
            ]
        }
    ]


def main():
    """
    Run the vision example.

    This function demonstrates how to:
    1. Set up the OpenAI API key
    2. Create a message with an image
    3. Send the message to a vision-capable model
    4. Process the response
    5. Send a follow-up question about the same image
    6. Display token usage information
    """
    # Set up API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for this example"
        )

    # Configure the API key for OpenAI
    set_api_key(api_key, "openai")

    # Sample image URL - replace with your own if needed
    image_url = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/"
        "Gfp-wisconsin-madison-the-nature-boardwalk.jpg/"
        "2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    )

    # Create messages with image
    messages = create_message_with_image(image_url)

    print("Sending request with an image to OpenAI's vision model...\n")

    # Call OpenAI with vision capabilities
    # We specify a vision-capable model and our messages containing the image
    response = ChatCompletion.create(
        model="openai/gpt-4-vision-preview",  # Use a vision-capable model
        messages=messages,
        max_tokens=300  # Limit the response length
    )

    # Print the response
    print("--- Vision Model Response ---")
    print(response.choices[0].message["content"])

    # Example of asking a follow-up question about the same image
    # We copy the original messages and add the assistant's response and a new user question
    follow_up_messages = messages.copy()
    follow_up_messages.append({
        "role": "assistant",
        "content": response.choices[0].message["content"]
    })
    follow_up_messages.append({
        "role": "user",
        "content": "What season does this image appear to be from?"
    })

    print("\nSending follow-up question...\n")

    # Send the follow-up question to the same model
    # The model will remember the context of the previous messages, including the image
    follow_up_response = ChatCompletion.create(
        model="openai/gpt-4-vision-preview",
        messages=follow_up_messages,
        max_tokens=100  # Shorter response for the follow-up
    )

    print("--- Follow-up Response ---")
    print(follow_up_response.choices[0].message["content"])

    # Display token usage information if available
    if response.usage:
        print(f"\nToken usage: {response.usage}")


if __name__ == "__main__":
    main()
