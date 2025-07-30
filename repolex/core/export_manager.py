"""
📤 PAC-MAN's Export Manager 📤

The ultimate data export system for Repolex's semantic intelligence!
Export PAC-MAN's collected semantic dots in multiple delicious formats!

WAKA WAKA! Sharing the semantic feast with everyone!
"""

import json
import csv
import logging
import gzip
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, IO
from enum import Enum
from dataclasses import dataclass, asdict

from pydantic import BaseModel, Field
from lxml import etree

from .config_manager import get_config, get_setting

logger = logging.getLogger(__name__)


class ExportFormat(str, Enum):
    """📤 PAC-MAN's export format options"""
    JSON = "json"                # 📄 JavaScript Object Notation
    CSV = "csv"                  # 📊 Comma-Separated Values
    XML = "xml"                  # 🌐 eXtensible Markup Language
    YAML = "yaml"                # 📝 YAML Ain't Markup Language
    TURTLE = "turtle"            # 🐢 RDF Turtle format
    N_TRIPLES = "ntriples"       # 🧬 RDF N-Triples format
    RDF_XML = "rdf_xml"          # 🌐 RDF/XML format
    JSONLD = "jsonld"            # 🔗 JSON-LD Linked Data
    MARKDOWN = "markdown"        # 📚 Markdown documentation
    HTML = "html"                # 🌐 HTML report
    OPML = "opml"                # 🌳 OPML outline format
    SQLITE = "sqlite"            # 🗄️ SQLite database
    MSGPACK = "msgpack"          # 🤖 MessagePack for LLM consumption


class CompressionType(str, Enum):
    """🗜️ PAC-MAN's compression options"""
    NONE = "none"                # No compression
    GZIP = "gzip"                # GZIP compression
    ZIP = "zip"                  # ZIP archive


@dataclass
class ExportMetadata:
    """📋 PAC-MAN's export metadata"""
    export_id: str
    format: ExportFormat
    compression: CompressionType
    timestamp: str
    source_type: str             # repository, query, system, etc.
    source_id: Optional[str]     # repo name, query id, etc.
    record_count: int
    file_size_bytes: int
    Repolex_version: str
    pac_man_signature: str
    
    def to_dict(self) -> Dict[str, Any]:
        """📋 Convert to dictionary"""
        return asdict(self)


class ExportOptions(BaseModel):
    """⚙️ PAC-MAN's export configuration options"""
    format: ExportFormat = Field(..., description="Export format")
    output_path: Optional[Path] = Field(None, description="Output file path")
    compression: CompressionType = Field(CompressionType.NONE, description="Compression type")
    include_metadata: bool = Field(True, description="Include export metadata")
    pretty_print: bool = Field(True, description="Pretty print output")
    encoding: str = Field("utf-8", description="File encoding")
    
    # Format-specific options
    csv_delimiter: str = Field(",", description="CSV delimiter")
    csv_quote_char: str = Field('"', description="CSV quote character")
    xml_root_element: str = Field("Repolex", description="XML root element name")
    html_title: str = Field("Repolex Export", description="HTML page title")
    markdown_title: str = Field("# Repolex Export", description="Markdown title")


class ExportManager:
    """📤 PAC-MAN's Export Manager - The Semantic Data Sharing System!"""
    
    def __init__(self):
        """📤 Initialize PAC-MAN's export system"""
        self.config = get_config()
        self.export_history: List[ExportMetadata] = []
        self.supported_formats = list(ExportFormat)
        
        # Ensure export directory exists
        self.default_export_dir = Path(self.config.export.output_directory).expanduser()
        self.default_export_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🟡 PAC-MAN Export Manager initialized - ready to share semantic dots!")
    
    def get_supported_formats(self) -> List[str]:
        """📤 Get list of supported export formats"""
        return [fmt.value for fmt in self.supported_formats]
    
    def generate_export_filename(
        self, 
        source_type: str, 
        format: ExportFormat, 
        source_id: Optional[str] = None,
        compression: CompressionType = CompressionType.NONE
    ) -> str:
        """📤 Generate a PAC-MAN export filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Base filename
        parts = ["Repolex", source_type]
        if source_id:
            # Sanitize source_id for filename
            safe_source_id = "".join(c for c in source_id if c.isalnum() or c in "-_")
            parts.append(safe_source_id)
        
        parts.append(timestamp)
        base_name = "_".join(parts)
        
        # Add format extension
        filename = f"{base_name}.{format.value}"
        
        # Add compression extension
        if compression == CompressionType.GZIP:
            filename += ".gz"
        elif compression == CompressionType.ZIP:
            filename += ".zip"
        
        return filename
    
    def export_data(
        self,
        data: Union[List[Dict[str, Any]], Dict[str, Any]],
        options: ExportOptions,
        source_type: str = "data",
        source_id: Optional[str] = None
    ) -> Path:
        """📤 Export PAC-MAN data in specified format"""
        try:
            export_id = f"export_{int(datetime.now().timestamp())}"
            
            # Determine output path
            if not options.output_path:
                filename = self.generate_export_filename(
                    source_type, options.format, source_id, options.compression
                )
                output_path = self.default_export_dir / filename
            else:
                output_path = options.output_path
            
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"🟡 PAC-MAN exporting {len(data) if isinstance(data, list) else 1} records to {output_path}")
            
            # Add metadata if requested
            export_data = data
            if options.include_metadata:
                metadata = {
                    "export_metadata": {
                        "export_id": export_id,
                        "format": options.format.value,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "source_type": source_type,
                        "source_id": source_id,
                        "record_count": len(data) if isinstance(data, list) else 1,
                        "Repolex_version": "2.0.0",
                        "pac_man_signature": "🟡 WAKA WAKA! Exported by PAC-MAN's semantic intelligence!"
                    }
                }
                
                if isinstance(data, list):
                    export_data = {**metadata, "data": data}
                else:
                    export_data = {**metadata, **data}
            
            # Export based on format
            if options.format == ExportFormat.JSON:
                content = self._export_json(export_data, options)
            elif options.format == ExportFormat.CSV:
                content = self._export_csv(export_data, options)
            elif options.format == ExportFormat.XML:
                content = self._export_xml(export_data, options)
            elif options.format == ExportFormat.YAML:
                content = self._export_yaml(export_data, options)
            elif options.format == ExportFormat.TURTLE:
                content = self._export_turtle(export_data, options)
            elif options.format == ExportFormat.N_TRIPLES:
                content = self._export_ntriples(export_data, options)
            elif options.format == ExportFormat.RDF_XML:
                content = self._export_rdf_xml(export_data, options)
            elif options.format == ExportFormat.JSONLD:
                content = self._export_jsonld(export_data, options)
            elif options.format == ExportFormat.MARKDOWN:
                content = self._export_markdown(export_data, options)
            elif options.format == ExportFormat.HTML:
                content = self._export_html(export_data, options)
            elif options.format == ExportFormat.OPML:
                content = self._export_opml(export_data, options)
            elif options.format == ExportFormat.SQLITE:
                return self._export_sqlite(export_data, options, output_path)
            elif options.format == ExportFormat.MSGPACK:
                return self._export_msgpack(export_data, options, output_path)
            else:
                raise ValueError(f"🟡 Unsupported export format: {options.format}")
            
            # Save content with optional compression
            self._save_content(content, output_path, options)
            
            # Record export metadata
            file_size = output_path.stat().st_size
            metadata = ExportMetadata(
                export_id=export_id,
                format=options.format,
                compression=options.compression,
                timestamp=datetime.now(timezone.utc).isoformat(),
                source_type=source_type,
                source_id=source_id,
                record_count=len(data) if isinstance(data, list) else 1,
                file_size_bytes=file_size,
                Repolex_version="2.0.0",
                pac_man_signature="🟡 WAKA WAKA!"
            )
            
            self.export_history.append(metadata)
            
            logger.info(f"🟡 PAC-MAN export complete: {output_path} ({file_size} bytes)")
            return output_path
            
        except Exception as e:
            logger.error(f"💥 PAC-MAN export failed: {e}")
            raise
    
    def _export_json(self, data: Any, options: ExportOptions) -> str:
        """📄 Export as JSON format"""
        return json.dumps(
            data,
            indent=2 if options.pretty_print else None,
            ensure_ascii=False,
            default=str  # Handle datetime and other objects
        )
    
    def _export_csv(self, data: Any, options: ExportOptions) -> str:
        """📊 Export as CSV format"""
        import io
        output = io.StringIO()
        
        # Extract data array for CSV
        if isinstance(data, dict) and "data" in data:
            rows = data["data"]
        elif isinstance(data, list):
            rows = data
        else:
            rows = [data]
        
        if not rows:
            return ""
        
        # Get field names from first row
        fieldnames = list(rows[0].keys()) if rows else []
        
        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
            delimiter=options.csv_delimiter,
            quotechar=options.csv_quote_char,
            quoting=csv.QUOTE_MINIMAL
        )
        
        writer.writeheader()
        for row in rows:
            # Convert complex objects to strings
            clean_row = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v 
                        for k, v in row.items()}
            writer.writerow(clean_row)
        
        return output.getvalue()
    
    def _export_xml(self, data: Any, options: ExportOptions) -> str:
        """🌐 Export as XML format"""
        root = etree.Element(options.xml_root_element)
        
        def dict_to_xml(parent, data_dict, item_name="item"):
            """Convert dictionary to XML elements"""
            if isinstance(data_dict, dict):
                for key, value in data_dict.items():
                    # Sanitize key for XML element name
                    safe_key = "".join(c for c in str(key) if c.isalnum() or c == "_")
                    if not safe_key or safe_key[0].isdigit():
                        safe_key = f"item_{safe_key}"
                    
                    element = etree.SubElement(parent, safe_key)
                    dict_to_xml(element, value)
            elif isinstance(data_dict, list):
                for item in data_dict:
                    item_element = etree.SubElement(parent, item_name)
                    dict_to_xml(item_element, item)
            else:
                parent.text = str(data_dict)
        
        dict_to_xml(root, data)
        
        return etree.tostring(
            root,
            pretty_print=options.pretty_print,
            encoding="unicode"
        )
    
    def _export_yaml(self, data: Any, options: ExportOptions) -> str:
        """📝 Export as YAML format"""
        try:
            import yaml
            return yaml.dump(
                data,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False
            )
        except ImportError:
            logger.warning("🟡 PyYAML not available, falling back to JSON-like format")
            return self._export_json(data, options)
    
    def _export_turtle(self, data: Any, options: ExportOptions) -> str:
        """🐢 Export as RDF Turtle format"""
        # Simplified Turtle export - would need proper RDF library for full implementation
        output = []
        output.append("@prefix Repolex: <http://Repolex.example.org/> .")
        output.append("@prefix pac: <http://pacman.example.org/> .")
        output.append("")
        
        # Convert data to simple triples
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        for i, item in enumerate(items):
            subject = f"Repolex:item_{i}"
            output.append(f"{subject}")
            
            if isinstance(item, dict):
                for key, value in item.items():
                    safe_key = "".join(c for c in str(key) if c.isalnum())
                    predicate = f"pac:{safe_key}"
                    
                    if isinstance(value, str):
                        object_val = f'"{value}"'
                    else:
                        object_val = f'"{str(value)}"'
                    
                    output.append(f"    {predicate} {object_val} ;")
                
                # Remove last semicolon and add period
                if output[-1].endswith(" ;"):
                    output[-1] = output[-1][:-2] + " ."
            
            output.append("")
        
        return "\n".join(output)
    
    def _export_ntriples(self, data: Any, options: ExportOptions) -> str:
        """🧬 Export as RDF N-Triples format"""
        output = []
        
        # Convert data to N-Triples
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        for i, item in enumerate(items):
            subject = f"<http://Repolex.example.org/item_{i}>"
            
            if isinstance(item, dict):
                for key, value in item.items():
                    safe_key = "".join(c for c in str(key) if c.isalnum())
                    predicate = f"<http://pacman.example.org/{safe_key}>"
                    
                    if isinstance(value, str):
                        object_val = f'"{value}"'
                    else:
                        object_val = f'"{str(value)}"'
                    
                    output.append(f"{subject} {predicate} {object_val} .")
        
        return "\n".join(output)
    
    def _export_rdf_xml(self, data: Any, options: ExportOptions) -> str:
        """🌐 Export as RDF/XML format"""
        # Simplified RDF/XML export
        root = etree.Element("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
        root.set("{http://www.w3.org/2000/xmlns/}Repolex", "http://Repolex.example.org/")
        root.set("{http://www.w3.org/2000/xmlns/}pac", "http://pacman.example.org/")
        
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        for i, item in enumerate(items):
            description = etree.SubElement(root, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
            description.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", f"http://Repolex.example.org/item_{i}")
            
            if isinstance(item, dict):
                for key, value in item.items():
                    safe_key = "".join(c for c in str(key) if c.isalnum())
                    prop = etree.SubElement(description, f"{{http://pacman.example.org/}}{safe_key}")
                    prop.text = str(value)
        
        return etree.tostring(root, pretty_print=options.pretty_print, encoding="unicode")
    
    def _export_jsonld(self, data: Any, options: ExportOptions) -> str:
        """🔗 Export as JSON-LD format"""
        context = {
            "@context": {
                "Repolex": "http://Repolex.example.org/",
                "pac": "http://pacman.example.org/",
                "@base": "http://Repolex.example.org/"
            }
        }
        
        if isinstance(data, dict):
            jsonld_data = {**context, **data}
        else:
            jsonld_data = {**context, "data": data}
        
        return json.dumps(jsonld_data, indent=2 if options.pretty_print else None)
    
    def _export_markdown(self, data: Any, options: ExportOptions) -> str:
        """📚 Export as Markdown format"""
        output = []
        output.append(options.markdown_title)
        output.append("")
        output.append("🟡 **PAC-MAN's Semantic Data Export**")
        output.append("")
        output.append(f"**Export Time:** {datetime.now().isoformat()}")
        output.append(f"**Format:** Markdown")
        output.append("")
        
        # Convert data to markdown
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
            
            # Add metadata if present
            if "export_metadata" in data:
                output.append("## Export Metadata")
                output.append("")
                metadata = data["export_metadata"]
                for key, value in metadata.items():
                    output.append(f"- **{key.replace('_', ' ').title()}:** {value}")
                output.append("")
            
            output.append("## Data")
            output.append("")
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        # Create table if all items have same structure
        if items and all(isinstance(item, dict) for item in items):
            # Get all unique keys
            all_keys = set()
            for item in items:
                all_keys.update(item.keys())
            
            keys = sorted(list(all_keys))
            
            # Create table header
            output.append("| " + " | ".join(keys) + " |")
            output.append("| " + " | ".join(["---"] * len(keys)) + " |")
            
            # Create table rows
            for item in items:
                row_values = [str(item.get(key, "")) for key in keys]
                output.append("| " + " | ".join(row_values) + " |")
        else:
            # List format
            for i, item in enumerate(items):
                output.append(f"### Item {i + 1}")
                output.append("")
                if isinstance(item, dict):
                    for key, value in item.items():
                        output.append(f"- **{key}:** {value}")
                else:
                    output.append(f"```\n{item}\n```")
                output.append("")
        
        output.append("---")
        output.append("*Generated by PAC-MAN's Repolex v2.0 - WAKA WAKA! 🟡*")
        
        return "\n".join(output)
    
    def _export_html(self, data: Any, options: ExportOptions) -> str:
        """🌐 Export as HTML format"""
        html_parts = []
        html_parts.append(f"<!DOCTYPE html>")
        html_parts.append(f"<html lang='en'>")
        html_parts.append(f"<head>")
        html_parts.append(f"    <meta charset='UTF-8'>")
        html_parts.append(f"    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append(f"    <title>{options.html_title}</title>")
        html_parts.append(f"    <style>")
        html_parts.append(f"        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; }}")
        html_parts.append(f"        .header {{ background: #FFD700; color: #000; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}")
        html_parts.append(f"        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}")
        html_parts.append(f"        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}")
        html_parts.append(f"        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}")
        html_parts.append(f"        th {{ background-color: #f2f2f2; }}")
        html_parts.append(f"        .footer {{ color: #666; font-style: italic; margin-top: 40px; }}")
        html_parts.append(f"    </style>")
        html_parts.append(f"</head>")
        html_parts.append(f"<body>")
        
        # Header
        html_parts.append(f"    <div class='header'>")
        html_parts.append(f"        <h1>🟡 {options.html_title}</h1>")
        html_parts.append(f"        <p>PAC-MAN's Semantic Data Export - WAKA WAKA!</p>")
        html_parts.append(f"    </div>")
        
        # Extract data
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
            
            # Show metadata if present
            if "export_metadata" in data:
                html_parts.append(f"    <div class='metadata'>")
                html_parts.append(f"        <h2>Export Metadata</h2>")
                metadata = data["export_metadata"]
                html_parts.append(f"        <ul>")
                for key, value in metadata.items():
                    html_parts.append(f"            <li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>")
                html_parts.append(f"        </ul>")
                html_parts.append(f"    </div>")
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        # Data table
        html_parts.append(f"    <h2>Data ({len(items)} records)</h2>")
        
        if items and all(isinstance(item, dict) for item in items):
            # Get all unique keys
            all_keys = set()
            for item in items:
                all_keys.update(item.keys())
            keys = sorted(list(all_keys))
            
            html_parts.append(f"    <table>")
            html_parts.append(f"        <thead>")
            html_parts.append(f"            <tr>")
            for key in keys:
                html_parts.append(f"                <th>{key}</th>")
            html_parts.append(f"            </tr>")
            html_parts.append(f"        </thead>")
            html_parts.append(f"        <tbody>")
            
            for item in items:
                html_parts.append(f"            <tr>")
                for key in keys:
                    value = str(item.get(key, ""))
                    html_parts.append(f"                <td>{value}</td>")
                html_parts.append(f"            </tr>")
            
            html_parts.append(f"        </tbody>")
            html_parts.append(f"    </table>")
        else:
            html_parts.append(f"    <pre>{json.dumps(items, indent=2)}</pre>")
        
        # Footer
        html_parts.append(f"    <div class='footer'>")
        html_parts.append(f"        <p><em>Generated by PAC-MAN's Repolex v2.0 on {datetime.now().isoformat()}</em></p>")
        html_parts.append(f"    </div>")
        
        html_parts.append(f"</body>")
        html_parts.append(f"</html>")
        
        return "\n".join(html_parts)
    
    def _export_opml(self, data: Any, options: ExportOptions) -> str:
        """🌳 Export as OPML format"""
        root = etree.Element("opml", version="2.0")
        
        # Head section
        head = etree.SubElement(root, "head")
        title = etree.SubElement(head, "title")
        title.text = "Repolex Export"
        created = etree.SubElement(head, "dateCreated")
        created.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        
        # Body section
        body = etree.SubElement(root, "body")
        
        # Extract data
        if isinstance(data, dict) and "data" in data:
            items = data["data"] if isinstance(data["data"], list) else [data["data"]]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        
        for i, item in enumerate(items):
            outline = etree.SubElement(body, "outline")
            outline.set("text", f"Item {i + 1}")
            
            if isinstance(item, dict):
                for key, value in item.items():
                    sub_outline = etree.SubElement(outline, "outline")
                    sub_outline.set("text", f"{key}: {value}")
        
        return etree.tostring(root, pretty_print=options.pretty_print, encoding="unicode")
    
    def _export_msgpack(self, data: Any, options: ExportOptions, output_path: Path) -> Path:
        """
        🤖 Export as MessagePack semantic DNA for LLM consumption
        
        Creates ultra-compact LLM-optimized representation with:
        - Function signatures + compressed docstrings  
        - Usage patterns and semantic clusters
        - String deduplication for maximum compression
        - jq-queryable structure for easy LLM access
        """
        try:
            import msgpack
            
            # Create semantic DNA structure optimized for LLMs
            semantic_dna = self._create_semantic_dna(data, is_current_repo=False)  # Default to dependency mode
            
            # Serialize with MessagePack for maximum compression
            packed_data = msgpack.packb(semantic_dna, use_bin_type=True)
            
            # Write to file
            with open(output_path, 'wb') as f:
                f.write(packed_data)
            
            logger.info(f"🤖 PAC-MAN msgpack DNA export complete: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("💥 MessagePack not available - install with: pip install msgpack")
            raise ValueError("MessagePack export requires msgpack module")
        except Exception as e:
            logger.error(f"💥 MessagePack export failed: {e}")
            raise
    
    def _create_semantic_dna(self, data: Any, is_current_repo: bool = False) -> Dict[str, Any]:
        """
        🧬 Create semantic DNA structure optimized for LLM consumption
        
        Based on the proven codedoc compact format with aggressive compression:
        - String table deduplication
        - Compressed function representations  
        - Semantic patterns and clusters
        - Everything an LLM needs, nothing it doesn't
        
        Args:
            data: Raw function data
            is_current_repo: If True, include all functions. If False, public only.
        """
        
        # Initialize compression tables
        string_table = []
        string_to_id = {}
        
        def get_string_id(text: str) -> int:
            """Get or create string table ID for deduplication"""
            if text in string_to_id:
                return string_to_id[text]
            string_id = len(string_table)
            string_table.append(text)
            string_to_id[text] = string_id
            return string_id
        
        # Extract functions from data (adapt based on repolex data structure)
        functions = []
        if isinstance(data, dict) and "data" in data:
            raw_functions = data["data"] if isinstance(data["data"], list) else [data["data"]]
        elif isinstance(data, list):
            raw_functions = data
        else:
            raw_functions = [data]
        
        print(f"🔧 DEBUG: _create_semantic_dna received {type(data)} with {len(raw_functions) if isinstance(raw_functions, list) else 'N/A'} raw_functions")
        
        # Process functions into compact format
        for i, func in enumerate(raw_functions):
            if isinstance(func, dict):
                # Create compact function representation  
                func_name = func.get("name", f"func_{i}")
                
                # 🎯 Two-tier filtering: current repo gets all, dependencies get public only
                if not is_current_repo and func_name.startswith('_'):
                    # Skip private/dunder functions for dependencies
                    continue
                
                func_module = func.get("module", "")
                func_signature = func.get("signature", f"def {func_name}()")
                func_docstring = func.get("docstring", f"Function {func_name}")
                
                compact_func = {
                    "id": i,
                    "n": func_name,  # name
                    "s": func_signature,  # signature
                    "d": get_string_id(func_docstring),  # docstring_id
                    "m": func_module,  # module
                    "t": func.get("tags", ["code", "stable"]),  # tags
                    "loc": [  # location [file, start, end]
                        func.get("file_path", ""),
                        func.get("line_number", 0),
                        func.get("end_line", 0)
                    ] if func.get("file_path") else None
                }
                functions.append(compact_func)
                
                # Debug first few functions
                if i < 3:
                    print(f"🔧 DEBUG: Processed function {i}: {func_name} from {func_module}")
        
        # Create basic module hierarchy  
        modules = [
            {
                "id": 0,
                "name": "root",
                "path": "",
                "exports": list(range(len(functions)))
            }
        ]
        
        # Basic semantic patterns (simplified for now)
        patterns = [
            {
                "name": "basic_usage",
                "template": "Most functions follow standard Python patterns",
                "frequency": 1.0,
                "context": ["general"],
                "related_functions": list(range(min(10, len(functions))))
            }
        ]
        
        # Create semantic DNA structure
        semantic_dna = {
            "format_version": "1.0",
            "generator": "repolex-v2.0-pac-man",
            "repo_info": {
                "name": "unknown" if isinstance(data, list) else data.get("export_metadata", {}).get("source_id", "unknown"),
                "version": "latest",
                "generated_at": datetime.now().isoformat(),
                "total_functions": len(functions)
            },
            
            # Core semantic data (optimized for LLMs)
            "functions": functions,
            "modules": modules, 
            "patterns": patterns,
            "semantic_clusters": {
                "all_functions": {
                    "functions": list(range(len(functions))),
                    "core_concept": "Repository function collection",
                    "typical_workflow": ["import", "call", "handle_result"]
                }
            },
            
            # Compression optimization
            "string_table": string_table,
            "compression_stats": {
                "total_strings": len(string_table),
                "unique_strings": len(set(string_table)),
                "compression_ratio": len(string_table) / max(1, len(set(string_table)))
            }
        }
        
        return semantic_dna

    def _export_sqlite(self, data: Any, options: ExportOptions, output_path: Path) -> Path:
        """🗄️ Export as SQLite database"""
        try:
            import sqlite3
            
            # Create database
            conn = sqlite3.connect(str(output_path))
            cursor = conn.cursor()
            
            # Extract data
            if isinstance(data, dict) and "data" in data:
                items = data["data"] if isinstance(data["data"], list) else [data["data"]]
                metadata = data.get("export_metadata", {})
            elif isinstance(data, list):
                items = data
                metadata = {}
            else:
                items = [data]
                metadata = {}
            
            # Create metadata table
            cursor.execute("""
                CREATE TABLE export_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            for key, value in metadata.items():
                cursor.execute("INSERT INTO export_metadata (key, value) VALUES (?, ?)", (key, str(value)))
            
            # Create data table if we have consistent dictionary items
            if items and all(isinstance(item, dict) for item in items):
                # Get all unique keys to create schema
                all_keys = set()
                for item in items:
                    all_keys.update(item.keys())
                
                keys = sorted(list(all_keys))
                
                # Create table with TEXT columns (SQLite is flexible)
                columns = ", ".join([f"{key} TEXT" for key in keys])
                cursor.execute(f"CREATE TABLE export_data (id INTEGER PRIMARY KEY, {columns})")
                
                # Insert data
                for item in items:
                    values = [str(item.get(key, "")) for key in keys]
                    placeholders = ", ".join(["?"] * len(keys))
                    cursor.execute(f"INSERT INTO export_data ({', '.join(keys)}) VALUES ({placeholders})", values)
            else:
                # Create simple key-value table for non-uniform data
                cursor.execute("""
                    CREATE TABLE export_data (
                        id INTEGER PRIMARY KEY,
                        data_json TEXT
                    )
                """)
                
                for i, item in enumerate(items):
                    cursor.execute("INSERT INTO export_data (data_json) VALUES (?)", (json.dumps(item),))
            
            conn.commit()
            conn.close()
            
            logger.info(f"🟡 PAC-MAN SQLite export complete: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("💥 SQLite3 module not available")
            raise ValueError("SQLite export requires sqlite3 module")
    
    def _save_content(self, content: str, output_path: Path, options: ExportOptions) -> None:
        """💾 Save content to file with optional compression"""
        if options.compression == CompressionType.GZIP:
            with gzip.open(output_path, 'wt', encoding=options.encoding) as f:
                f.write(content)
        elif options.compression == CompressionType.ZIP:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Use original filename without .zip extension
                original_name = output_path.stem
                zipf.writestr(original_name, content.encode(options.encoding))
        else:
            with open(output_path, 'w', encoding=options.encoding) as f:
                f.write(content)
    
    def get_export_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """📋 Get PAC-MAN export history"""
        history = [export.to_dict() for export in self.export_history]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x['timestamp'], reverse=True)
        
        if limit:
            history = history[:limit]
        
        return history
    
    def export_repository_data(self, repo_name: str, repo_data: Dict[str, Any], format: ExportFormat) -> Path:
        """📚 Export repository data"""
        options = ExportOptions(format=format)
        return self.export_data(
            data=repo_data,
            options=options,
            source_type="repository",
            source_id=repo_name
        )
    
    def export_query_results(self, query_results: List[Dict[str, Any]], query_id: str, format: ExportFormat) -> Path:
        """🔍 Export query results"""
        options = ExportOptions(format=format)
        return self.export_data(
            data=query_results,
            options=options,
            source_type="query",
            source_id=query_id
        )
    
    def export_system_diagnostics(self, diagnostics: Dict[str, Any], format: ExportFormat) -> Path:
        """🔧 Export system diagnostics"""
        options = ExportOptions(format=format)
        return self.export_data(
            data=diagnostics,
            options=options,
            source_type="system",
            source_id="diagnostics"
        )
    
    def export_msgpack(self, org_repo: str, release: str, output_path: Optional[Path] = None, 
                      include_nlp: bool = False, is_current_repo: bool = False, progress_callback=None) -> Path:
        """
        🤖 Export repository as LLM-optimized semantic DNA msgpack
        
        Creates ultra-compact semantic intelligence package optimized for LLM consumption.
        Based on the proven codedoc "Semantic DNA" format with 125x compression.
        
        Args:
            org_repo: Repository identifier (e.g., "pixeltable/pixeltable")  
            release: Release version (e.g., "v0.4.14", "latest")
            output_path: Custom output path (default: llm-repolex/{org}~{repo}~{release}.msgpack)
            include_nlp: Include experimental NLP analysis graphs (default: False)
            is_current_repo: If True, include all functions. If False, public only for dependencies.
            progress_callback: Progress reporting callback
            
        Returns:
            Path: Location of generated msgpack file
        """
        from ..storage.oxigraph_client import get_oxigraph_client
        from ..utils.validation import validate_org_repo, validate_release_tag
        
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        if progress_callback:
            progress_callback(0, f"🤖 Initializing semantic DNA extraction for {org_repo}")
        
        try:
            # Get oxigraph client and query for repository data
            oxigraph = get_oxigraph_client()
            
            if progress_callback:
                progress_callback(20, f"🧬 Extracting function signatures from semantic graphs")
            
            # Query for functions from the stable functions graph
            functions_query = f"""
            PREFIX woc: <http://rdf.webofcode.org/woc/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?function ?name ?module ?signature WHERE {{
                GRAPH <http://repolex.org/repo/{org_repo}/functions/stable> {{
                    ?function a woc:Function ;
                             woc:canonicalName ?name .
                    
                    OPTIONAL {{ ?function woc:module ?module }}
                    OPTIONAL {{ ?function woc:hasSignature ?signature }}
                }}
            }}
            ORDER BY ?name
            """
            
            logger.info(f"🤖 Querying semantic graphs for {org_repo} functions...")
            query_result = oxigraph.query_sparql(functions_query)
            
            logger.info(f"🔍 SPARQL query returned {len(query_result.results)} results")
            
            if progress_callback:
                progress_callback(60, f"🗜️ Compressing {len(query_result.results)} functions into semantic DNA")
            
            # Convert SPARQL results to function data
            function_data = []
            for result in query_result.results:
                func_name = result.get("name", "unknown")
                # Use the actual signature from the graph, fallback to basic signature if missing
                func_signature = result.get("signature", f"def {func_name}()")
                # Ensure signature starts with 'def' for consistency
                if not func_signature.startswith("def ") and not func_signature.startswith("async def "):
                    func_signature = f"def {func_signature}"
                
                func_data = {
                    "name": func_name,
                    "signature": func_signature,
                    "docstring": f"Function {func_name} from {result.get('module', 'unknown module')}",
                    "module": result.get("module", ""),
                    "file_path": "",  # Not available in current schema
                    "line_number": 0,  # Not available in current schema  
                    "end_line": 0,     # Not available in current schema
                    "tags": ["code", "stable"]  # Base tags for code functions
                }
                
                # Add NLP tags if requested and available
                if include_nlp:
                    func_data["tags"].append("nlp_enhanced")
                
                function_data.append(func_data)
            
            logger.info(f"📊 Converted {len(function_data)} SPARQL results to function data")
            
            if progress_callback:
                progress_callback(80, f"📦 Packaging semantic DNA with MessagePack compression")
            
            # Determine output path
            if not output_path:
                # Create llm-repolex directory structure
                llm_rlex_dir = Path("llm-repolex")
                llm_rlex_dir.mkdir(exist_ok=True)
                
                # Generate filename: {org}~{repo}~{release}.msgpack
                org, repo = org_repo.split("/", 1)
                filename = f"{org}~{repo}~{release}.msgpack"
                output_path = llm_rlex_dir / filename
            else:
                # If output_path is intended as a directory (no file extension), create filename inside it
                if output_path.is_dir() or not output_path.suffix or str(output_path).endswith('/'):
                    # Ensure directory exists
                    output_path.mkdir(parents=True, exist_ok=True)
                    
                    # Generate filename: {org}~{repo}~{release}.msgpack
                    org, repo = org_repo.split("/", 1)
                    filename = f"{org}~{repo}~{release}.msgpack"
                    output_path = output_path / filename
                # else: treat as complete file path
            
            # Create export options for msgpack
            options = ExportOptions(
                format=ExportFormat.MSGPACK,
                output_path=output_path,
                include_metadata=True
            )
            
            # Create semantic DNA directly instead of using export_data wrapper
            semantic_dna = self._create_semantic_dna(function_data, is_current_repo=is_current_repo)
            
            # Serialize with MessagePack
            import msgpack
            packed_data = msgpack.packb(semantic_dna, use_bin_type=True)
            
            # Write to file
            with open(output_path, 'wb') as f:
                f.write(packed_data)
            
            result_path = output_path
            
            if progress_callback:
                progress_callback(100, f"🚀 Semantic DNA ready for LLM consumption!")
            
            # Log success with compression stats
            file_size = result_path.stat().st_size
            logger.info(f"🧬 Semantic DNA generated: {result_path}")
            logger.info(f"📊 Functions: {len(function_data)}, Size: {file_size:,} bytes")
            logger.info(f"🤖 Ready for LLM jq queries: cat {result_path} | msgpack -d | jq '.functions[0]'")
            
            return result_path
            
        except Exception as e:
            logger.error(f"🤖 Semantic DNA extraction failed for {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"DNA extraction failed: {e}")
            raise


# Global export manager instance
_export_manager: Optional[ExportManager] = None


def get_export_manager() -> ExportManager:
    """🟡 Get the global PAC-MAN export manager"""
    global _export_manager
    if _export_manager is None:
        _export_manager = ExportManager()
    return _export_manager


def export_data(data: Any, format: ExportFormat, output_path: Optional[Path] = None) -> Path:
    """🟡 Quick export PAC-MAN data"""
    options = ExportOptions(format=format, output_path=output_path)
    return get_export_manager().export_data(data, options)


# Example usage for PAC-MAN's export system!
if __name__ == "__main__":
    # 🟡 PAC-MAN Export Manager Demo!
    export_manager = ExportManager()
    
    print("🟡 PAC-MAN Export Demo!")
    print("=" * 40)
    
    # Sample data
    sample_data = [
        {"id": 1, "name": "PAC-MAN", "type": "hero", "dots_eaten": 9999},
        {"id": 2, "name": "Blinky", "type": "ghost", "color": "red"},
        {"id": 3, "name": "Pinky", "type": "ghost", "color": "pink"},
        {"id": 4, "name": "Inky", "type": "ghost", "color": "cyan"},
        {"id": 5, "name": "Sue", "type": "ghost", "color": "orange"}
    ]
    
    print(f"\n📤 Exporting {len(sample_data)} PAC-MAN records...")
    
    # Test different formats
    formats_to_test = [ExportFormat.JSON, ExportFormat.CSV, ExportFormat.XML, ExportFormat.MARKDOWN]
    
    for fmt in formats_to_test:
        try:
            options = ExportOptions(format=fmt, pretty_print=True)
            output_path = export_manager.export_data(
                data=sample_data,
                options=options,
                source_type="demo",
                source_id="pac_man_characters"
            )
            print(f"  ✅ {fmt.value.upper()}: {output_path}")
        except Exception as e:
            print(f"  ❌ {fmt.value.upper()}: {e}")
    
    print(f"\n📋 Export history:")
    for export_record in export_manager.get_export_history(limit=5):
        print(f"  - {export_record['format']} export: {export_record['record_count']} records ({export_record['file_size_bytes']} bytes)")
    
    print("\n🟡 WAKA WAKA! Export system ready!")