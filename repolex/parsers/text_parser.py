"""
🛸 MOTHERSHIP TEXT INTELLIGENCE SCANNER 🛸

Advanced NLP analysis for text repositories - where no LLM has gone before!
Boldly extracting entities, relationships, and semantic structures from the cosmic text frontier.

The Text Parser complements our code analysis with deep semantic understanding of:
- Documentation repositories (GitBook, Sphinx, etc.)
- Creative writing projects
- Blog/content repositories  
- Research papers and knowledge bases
- Mixed code+docs repositories

Components:
- Entity extraction using GLiNER
- Relationship discovery
- Content structure analysis
- Semantic concept mapping
"""

import logging
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import re
from collections import defaultdict

# NLP dependencies (will be optional imports)
try:
    from gliner import GLiNER
    GLINER_AVAILABLE = True
except ImportError:
    GLINER_AVAILABLE = False
    GLiNER = None

from ..models.function import DocumentInfo, EntityInfo, RelationshipInfo
from ..models.exceptions import ParsingError, ValidationError


logger = logging.getLogger(__name__)


@dataclass
class EntityExtraction:
    """Information about an extracted entity."""
    text: str
    label: str  # PERSON, ORGANIZATION, LOCATION, CONCEPT, etc.
    start_pos: int
    end_pos: int
    confidence: float
    context: str  # Surrounding text for context


@dataclass
class RelationshipExtraction:
    """Information about discovered relationships between entities."""
    source_entity: str
    target_entity: str
    relationship_type: str  # MENTIONS, REFERENCES, RELATES_TO, etc.
    context: str
    confidence: float


@dataclass
class DocumentStructure:
    """Analysis of document structure and hierarchy."""
    title: Optional[str] = None
    headings: List[Tuple[int, str]] = field(default_factory=list)  # (level, text)
    sections: List[Dict[str, Any]] = field(default_factory=list)
    word_count: int = 0
    reading_time_minutes: int = 0
    language: str = "en"
    topics: List[str] = field(default_factory=list)


class TextParser:
    """
    🛸 MOTHERSHIP TEXT INTELLIGENCE SCANNER 🛸
    
    Advanced NLP analysis pipeline for semantic text understanding.
    Extracts entities, relationships, and document structure from text files.
    """
    
    def __init__(self, enable_advanced_nlp: bool = True):
        """
        Initialize the text analysis pipeline.
        
        Args:
            enable_advanced_nlp: Whether to enable GLiNER and advanced NLP features
        """
        self.enable_advanced_nlp = enable_advanced_nlp
        self._gliner_model = None
        
        # Entity types we want to extract
        self.entity_types = [
            "PERSON", "ORGANIZATION", "LOCATION", "CONCEPT", 
            "TECHNOLOGY", "PRODUCT", "EVENT", "DATE", "URL"
        ]
        
        # 🧠 MOOD/EMOTION entity types for psychological analysis
        self.mood_types = [
            "PASSIONATE", "THOUGHTFUL", "CURIOUS", "EXCITED", "ANXIOUS", 
            "FOCUSED", "DETERMINED", "CONTEMPLATIVE", "ENTHUSIASTIC",
            "ANALYTICAL", "CREATIVE", "INTROSPECTIVE", "MEDITATIVE",
            "OPTIMISTIC", "PESSIMISTIC", "CONFIDENT", "UNCERTAIN"
        ]
        
        # Initialize models if available
        if self.enable_advanced_nlp and GLINER_AVAILABLE:
            logger.info("🛸 MOTHERSHIP: Initializing GLiNER entity scanner...")
            self._initialize_gliner()
        else:
            logger.info("🛸 MOTHERSHIP: Running in basic text analysis mode")
    
    def _initialize_gliner(self):
        """Initialize GLiNER model for entity extraction."""
        try:
            # Use a lightweight GLiNER model suitable for general entity extraction
            self._gliner_model = GLiNER.from_pretrained("urchade/gliner_base")
            logger.info("👽 GLiNER entity scanner online and ready for cosmic text probing!")
        except Exception as e:
            logger.warning(f"🛸 MOTHERSHIP: GLiNER initialization failed: {e}")
            logger.info("🛸 Falling back to basic text analysis mode")
            self.enable_advanced_nlp = False
    
    def _preprocess_text(self, content: str) -> str:
        """🚀 SLOPAT OPTIMIZATION: Clean and prepare text for GLiNER extraction"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove markdown formatting that might confuse GLiNER
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic  
        content = re.sub(r'`(.*?)`', r'\1', content)        # Inline code
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code blocks
        
        # Remove JSON-like braces that might confuse consciousness analysis
        content = re.sub(r'\{[^}]*\}', '', content)
        
        return content.strip()

    def analyze_text_file(self, file_path: Path, content: str) -> DocumentInfo:
        """
        🛸 PRIME DIRECTIVE: Analyze a text file for semantic intelligence
        
        Args:
            file_path: Path to the text file
            content: File content as string
            
        Returns:
            DocumentInfo: Complete semantic analysis of the text
        """
        logger.info(f"🛸 MOTHERSHIP: Scanning {file_path.name} for alien intelligence...")
        
        try:
            # Basic document structure analysis
            structure = self._analyze_document_structure(content)
            logger.info(f"📊 Document structure decoded: {len(structure.headings)} sections, {structure.word_count} words")
            
            # Extract entities if advanced NLP is enabled
            entities = []
            if self.enable_advanced_nlp and self._gliner_model:
                entities = self._extract_entities(content)
                logger.info(f"👽 Discovered {len(entities)} alien entities in the cosmic text!")
            
            # Discover relationships between entities
            relationships = []
            if entities:
                relationships = self._discover_relationships(content, entities)
                logger.info(f"🔗 Mapped {len(relationships)} interdimensional relationships!")
            
            # Create document info
            doc_info = DocumentInfo(
                file_path=str(file_path),
                title=structure.title,
                word_count=structure.word_count,
                reading_time_minutes=structure.reading_time_minutes,
                language=structure.language,
                headings=structure.headings,
                entities=entities,
                relationships=relationships,
                topics=structure.topics,
                structure_analysis=structure.dict() if hasattr(structure, 'dict') else structure.__dict__
            )
            
            logger.info(f"🚀 MISSION COMPLETE: {file_path.name} successfully analyzed!")
            return doc_info
            
        except Exception as e:
            raise ParsingError(
                f"🛸 MOTHERSHIP: Text analysis failed for {file_path}: {e}",
                suggestions=[
                    "Check if file encoding is UTF-8",
                    "Verify file is not corrupted",
                    "Try with --nlp=false for basic analysis"
                ]
            )
    
    def _analyze_document_structure(self, content: str) -> DocumentStructure:
        """Analyze document structure, headings, and basic metrics."""
        lines = content.split('\n')
        
        # Extract title (first H1 or first non-empty line)
        title = None
        headings = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Markdown headings
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_text = line.lstrip('#').strip()
                headings.append((level, heading_text))
                
                if not title and level == 1:
                    title = heading_text
            
            # First significant line as title if no H1 found
            elif not title and len(line) > 10:
                title = line[:100]  # Truncate long titles
        
        # Basic metrics
        words = content.split()
        word_count = len(words)
        reading_time = max(1, word_count // 200)  # ~200 WPM average
        
        # Simple topic extraction (basic keyword frequency)
        topics = self._extract_basic_topics(content)
        
        return DocumentStructure(
            title=title,
            headings=headings,
            word_count=word_count,
            reading_time_minutes=reading_time,
            language="en",  # TODO: Add language detection
            topics=topics
        )
    
    def _extract_entities(self, content: str) -> List[EntityExtraction]:
        """Extract named entities and mood/emotion entities using GLiNER."""
        if not self._gliner_model:
            return []
        
        try:
            # 🚀 SLOPAT OPTIMIZATION: Preprocess text to improve GLiNER performance
            cleaned_content = self._preprocess_text(content)
            logger.info(f"🧹 Cleaned text: {len(content)} → {len(cleaned_content)} chars")
            
            # Split content into chunks to avoid memory issues
            chunks = self._chunk_text(cleaned_content, max_length=512)
            all_entities = []
            
            for chunk_start, chunk_text in chunks:
                # 👽🧠 Extract ALL entities in one pass (regular + mood) for efficiency
                all_entity_types = self.entity_types + self.mood_types
                entities = self._gliner_model.predict_entities(
                    chunk_text, 
                    all_entity_types,
                    threshold=0.3  # 🚀 SLOPAT OPTIMIZATION: Higher threshold for performance!
                )
                
                # Convert all entities to our format
                for entity in entities:
                    # Check if this is a mood entity
                    if entity["label"] in self.mood_types:
                        label = f"MOOD_{entity['label']}"  # Prefix mood entities
                    else:
                        label = entity["label"]  # Regular entity
                    
                    entity_info = EntityExtraction(
                        text=entity["text"],
                        label=label,
                        start_pos=chunk_start + entity["start"],
                        end_pos=chunk_start + entity["end"],
                        confidence=entity.get("score", 0.0),
                        context=self._get_entity_context(cleaned_content, 
                                                       chunk_start + entity["start"],
                                                       chunk_start + entity["end"])
                    )
                    all_entities.append(entity_info)
            
            logger.info(f"🧠 Extracted {len([e for e in all_entities if e.label.startswith('MOOD_')])} mood entities!")
            
            # Deduplicate similar entities
            return self._deduplicate_entities(all_entities)
            
        except Exception as e:
            logger.warning(f"👽 Entity extraction probe malfunction: {e}")
            return []
    
    def _discover_relationships(self, content: str, entities: List[EntityExtraction]) -> List[RelationshipExtraction]:
        """Discover relationships between extracted entities."""
        relationships = []
        
        # Simple co-occurrence based relationship discovery
        # More sophisticated models could be added here
        
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if entity1.label != entity2.label:  # Different types
                    # Check if entities appear in same paragraph/context
                    distance = abs(entity1.start_pos - entity2.start_pos)
                    if distance < 500:  # Within ~500 characters
                        rel_type = self._infer_relationship_type(entity1, entity2, content)
                        if rel_type:
                            relationships.append(RelationshipExtraction(
                                source_entity=entity1.text,
                                target_entity=entity2.text,
                                relationship_type=rel_type,
                                context=self._get_relationship_context(content, entity1, entity2),
                                confidence=0.7  # Basic heuristic confidence
                            ))
        
        return relationships
    
    def _chunk_text(self, text: str, max_length: int = 256) -> List[Tuple[int, str]]:
        """Split text into overlapping chunks for processing."""
        chunks = []
        start = 0
        overlap = 50  # Character overlap between chunks
        
        while start < len(text):
            end = min(start + max_length, len(text))
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = text.rfind('.', start, end)
                if last_period > start + max_length // 2:
                    end = last_period + 1
            
            chunks.append((start, text[start:end]))
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def _get_entity_context(self, content: str, start: int, end: int, window: int = 50) -> str:
        """Get surrounding context for an entity."""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end].strip()
    
    def _get_relationship_context(self, content: str, entity1: EntityExtraction, entity2: EntityExtraction) -> str:
        """Get context showing relationship between two entities."""
        start = min(entity1.start_pos, entity2.start_pos)
        end = max(entity1.end_pos, entity2.end_pos)
        
        # Expand context window
        context_start = max(0, start - 100)
        context_end = min(len(content), end + 100)
        
        return content[context_start:context_end].strip()
    
    def _infer_relationship_type(self, entity1: EntityExtraction, entity2: EntityExtraction, content: str) -> Optional[str]:
        """Infer relationship type between entities using simple heuristics."""
        # This is a simplified approach - could be enhanced with ML models
        
        context = self._get_relationship_context(content, entity1, entity2).lower()
        
        # Simple pattern matching for common relationships
        if any(word in context for word in ["created", "developed", "built", "founded"]):
            return "CREATED_BY"
        elif any(word in context for word in ["works at", "employed by", "member of"]):
            return "WORKS_AT"
        elif any(word in context for word in ["located in", "based in", "from"]):
            return "LOCATED_IN"
        elif any(word in context for word in ["uses", "utilizes", "implements"]):
            return "USES"
        elif any(word in context for word in ["mentions", "refers to", "discusses"]):
            return "MENTIONS"
        else:
            return "RELATED_TO"  # Generic relationship
    
    def _deduplicate_entities(self, entities: List[EntityExtraction]) -> List[EntityExtraction]:
        """Remove duplicate or very similar entities."""
        deduplicated = []
        seen_texts = set()
        
        for entity in entities:
            # Simple deduplication by exact text match
            if entity.text.lower() not in seen_texts:
                seen_texts.add(entity.text.lower())
                deduplicated.append(entity)
        
        return deduplicated
    
    def _extract_basic_topics(self, content: str, max_topics: int = 5) -> List[str]:
        """Extract basic topics using keyword frequency analysis."""
        # Remove common words and extract frequent terms
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        
        # Common stopwords to filter out
        stopwords = {
            'that', 'this', 'with', 'from', 'they', 'been', 'have', 'were', 
            'said', 'each', 'which', 'their', 'time', 'will', 'about', 'would',
            'there', 'could', 'other', 'after', 'first', 'well', 'also', 'more'
        }
        
        # Count word frequencies
        word_freq = defaultdict(int)
        for word in words:
            if word not in stopwords and len(word) > 3:
                word_freq[word] += 1
        
        # Get top frequent words as topics
        topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [topic[0] for topic in topics[:max_topics]]


def create_text_parser(enable_nlp: bool = True) -> TextParser:
    """
    🛸 MOTHERSHIP FACTORY: Create a text analysis parser
    
    Args:
        enable_nlp: Whether to enable advanced NLP features
        
    Returns:
        TextParser: Ready for cosmic text analysis
    """
    logger.info("🛸 MOTHERSHIP: Assembling text analysis probe...")
    return TextParser(enable_advanced_nlp=enable_nlp)