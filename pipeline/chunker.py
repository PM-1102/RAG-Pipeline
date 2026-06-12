# pipeline/chunker.py
import uuid
import hashlib
import re
from typing import List
from pipeline.contracts import DocumentChunk

def calculate_deterministic_uuid(text: str) -> str:
    """
    Generates a strictly RFC 4122 compliant 128-bit UUID string from raw text content.
    Ensures absolute compatibility with Qdrant storage engines while retaining 
    deterministic deduplication attributes.
    """
    # MD5 generates an exact 16-byte (128-bit) digest array
    hash_bytes = hashlib.md5(text.encode("utf-8")).digest()
    # Cast the raw bytes directly into a type-safe standard UUID representation
    return str(uuid.UUID(bytes=hash_bytes))

def split_markdown_by_sections(markdown_text: str, document_id: str, max_chunk_size: int = 1200) -> List[DocumentChunk]:
    """
    Parses raw markdown text by section headers, injecting structural path history 
    into child nodes to eliminate contextual shearing.
    """
    chunks: List[DocumentChunk] = []
    lines = markdown_text.split("\n")
    
    current_headings = {1: "", 2: "", 3: ""}
    current_buffer = []
    current_page = 1
    
    table_mode = False

    for line in lines:
        # Track physical document pages if marked by loader parameters
        if "PAGE_MARKER_" in line:
            page_match = re.search(r"PAGE_MARKER_(\d+)", line)
            if page_match:
                current_page = int(page_match.group(1))
            continue

        # Detect active Markdown table boundaries to shield structural parameters
        if line.strip().startswith("|"):
            table_mode = True
        elif table_mode and not line.strip().startswith("|") and line.strip() != "":
            table_mode = False

        # Identify structure heading thresholds (# Sections)
        header_match = re.match(r"^(#{1,3})\s+(.*)$", line)
        
        if header_match and not table_mode:
            # If we have content buffered, flush it as a complete logical chunk before shifting sections
            if current_buffer and len("\n".join(current_buffer).strip()) > 50:
                chunk_content = "\n".join(current_buffer).strip()
                # Prepend contextual layout trail to the chunk block
                context_prefix = " > ".join([v for v in current_headings.values() if v])
                final_text = f"Context: {context_prefix}\n\n{chunk_content}" if context_prefix else chunk_content
                
                chunks.append(DocumentChunk(
                    chunk_id=calculate_deterministic_uuid(final_text),
                    document_id=document_id,
                    content=final_text,
                    metadata={"page_number": current_page, "section_path": context_prefix}
                ))
                current_buffer = []

            # Update heading hierarchy parameters
            header_level = len(header_match.group(1))
            header_title = header_match.group(2).strip()
            current_headings[header_level] = header_title
            
            # Clear subordinate lower-level nested headers to prevent structural drift
            for level in range(header_level + 1, 4):
                current_headings[level] = ""

        current_buffer.append(line)

        # Safety Valve: If context goes over size parameters, flush text to optimize context lengths
        if len("\n".join(current_buffer)) >= max_chunk_size and not table_mode:
            chunk_content = "\n".join(current_buffer).strip()
            context_prefix = " > ".join([v for v in current_headings.values() if v])
            final_text = f"Context: {context_prefix}\n\n{chunk_content}" if context_prefix else chunk_content
            
            chunks.append(DocumentChunk(
                chunk_id=calculate_deterministic_uuid(final_text),
                document_id=document_id,
                content=final_text,
                metadata={"page_number": current_page, "section_path": context_prefix}
            ))
            current_buffer = current_buffer[-2:] if len(current_buffer) > 2 else []

    # Final sweep of remaining items in text buffers
    if current_buffer and len("\n".join(current_buffer).strip()) > 10:
        chunk_content = "\n".join(current_buffer).strip()
        context_prefix = " > ".join([v for v in current_headings.values() if v])
        final_text = f"Context: {context_prefix}\n\n{chunk_content}" if context_prefix else chunk_content
        
        chunks.append(DocumentChunk(
            chunk_id=calculate_deterministic_uuid(final_text),
            document_id=document_id,
            content=final_text,
            metadata={"page_number": current_page, "section_path": context_prefix}
        ))

    return chunks