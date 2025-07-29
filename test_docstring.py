"""
Test file with rich docstrings for our enhanced parser!
"""

def complex_algorithm(data, threshold=0.5, optimize=True):
    """Advanced data processing algorithm with comprehensive documentation.
    
    This function performs sophisticated data analysis using machine learning
    techniques to identify patterns and optimize performance.
    
    Args:
        data: Input dataset for processing #data #ml
        threshold: Confidence threshold for predictions
        optimize: Whether to enable performance optimizations
    
    Returns:
        Processed results with confidence scores
    
    Raises:
        ValueError: If data is empty or invalid
        RuntimeError: If optimization fails
    
    Examples:
        Basic usage:
        >>> result = complex_algorithm([1, 2, 3])
        >>> print(result)
        
        With custom threshold:
        >>> result = complex_algorithm(data, threshold=0.8)
    
    Author:
        Dr. Jane Smith <jane@example.com>
    
    Since:
        v1.2.0
        
    Version:
        v2.1.0
    
    Complexity:
        O(n log n) time, O(n) space
        
    Performance:
        Optimized for large datasets, uses vectorized operations
        
    Memory:
        Approximately 2x input size during processing
    
    Todo:
        - Add support for streaming data
        - Implement parallel processing
        - Add GPU acceleration
    
    Notes:
        - Function is thread-safe
        - Caches intermediate results
        - Requires numpy >= 1.20.0
    
    Warnings:
        - Large datasets may cause memory issues
        - Threshold values below 0.1 may produce unreliable results
    
    See Also:
        - preprocess_data: Data preparation function
        - validate_results: Result validation utility
    
    References:
        - [Smith et al. 2023] "Advanced ML Algorithms"
        - https://example.com/algorithm-docs
    
    Test Examples:
        - Basic functionality tested with synthetic data
        - Performance tested with 1M+ records
        - Edge cases: empty data, NaN values, extreme thresholds
    
    Known Issues:
        - Memory leak with very large datasets (>10GB)
        - Numerical instability with threshold=1.0
    
    Usage Patterns:
        - Most common: complex_algorithm(data, threshold=0.7)
        - Batch processing: [complex_algorithm(chunk) for chunk in chunks]
    
    Best Practices:
        - Always validate input data first
        - Use threshold >= 0.2 for stable results
        - Enable optimization for datasets > 1000 records
    
    @experimental - This algorithm is still in beta
    @tested - Full test coverage available
    """
    # Implementation would go here
    return {"processed": True, "confidence": threshold}


def deprecated_function():
    """Old function that should not be used anymore.
    
    Deprecated: This function is deprecated since v2.0.0 and will be removed in v3.0.0.
    Use new_improved_function() instead.
    
    @deprecated
    @internal
    """
    pass