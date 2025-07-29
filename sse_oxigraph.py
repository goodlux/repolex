#!/usr/bin/env python3
"""
SSE wrapper for mcp-server-oxigraph
"""
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the mcp-server-oxigraph to the path
sys.path.insert(0, '/Users/rob/repos/mcp-server-oxigraph/src')

def main():
    """Run oxigraph MCP server with SSE transport"""
    # Set up environment
    os.environ.setdefault('OXIGRAPH_DEFAULT_STORE', '/Users/rob/.claude-code/oxigraph')
    
    logger.info("Starting SSE Oxigraph MCP server")
    
    # Import all the components from the original server
    from mcp.server.fastmcp import FastMCP
    from mcp_server_oxigraph.utils import setup_resilient_process
    from mcp_server_oxigraph.core.config import get_default_store_path, get_system_default_store_path
    from mcp_server_oxigraph.core.store import (
        oxigraph_create_store, oxigraph_open_store, oxigraph_close_store,
        oxigraph_backup_store, oxigraph_restore_store, oxigraph_optimize_store,
        oxigraph_list_stores, oxigraph_get_store
    )
    from mcp_server_oxigraph.core.rdf import (
        oxigraph_create_named_node, oxigraph_create_blank_node, oxigraph_create_literal,
        oxigraph_create_quad, oxigraph_add, oxigraph_add_many, oxigraph_remove,
        oxigraph_remove_many, oxigraph_clear, oxigraph_quads_for_pattern
    )
    from mcp_server_oxigraph.core.sparql import (
        oxigraph_query, oxigraph_update, oxigraph_query_with_options,
        oxigraph_prepare_query, oxigraph_execute_prepared_query, oxigraph_run_query
    )
    from mcp_server_oxigraph.core.format import (
        oxigraph_parse, oxigraph_serialize, oxigraph_import_file,
        oxigraph_export_graph, oxigraph_get_supported_formats
    )
    
    # Create SSE-enabled MCP server
    mcp = FastMCP(name="oxigraph", version="0.1.0")
    
    # Initialize stores like the original
    try:
        user_path = get_default_store_path()
        if user_path:
            try:
                logger.info(f"Creating/opening user default store at: {user_path}")
                result = oxigraph_create_store(user_path)
                logger.info(f"Default store: {result.get('store', user_path)}")
            except Exception as e:
                logger.error(f"Failed to create user default store: {e}")
        
        system_path = get_system_default_store_path()
        try:
            logger.info(f"Creating/opening system default store at: {system_path}")
            result = oxigraph_create_store(system_path)
            logger.info(f"System default store: {result.get('store', system_path)}")
        except Exception as e:
            logger.error(f"Failed to create system default store: {e}")
    except Exception as e:
        logger.error(f"Error initializing default stores: {e}")
    
    # Register all the tools (same as original server)
    mcp.tool()(oxigraph_create_store)
    mcp.tool()(oxigraph_open_store)
    mcp.tool()(oxigraph_close_store)
    mcp.tool()(oxigraph_backup_store)
    mcp.tool()(oxigraph_restore_store)
    mcp.tool()(oxigraph_optimize_store)
    mcp.tool()(oxigraph_list_stores)
    
    mcp.tool()(oxigraph_create_named_node)
    mcp.tool()(oxigraph_create_blank_node)
    mcp.tool()(oxigraph_create_literal)
    mcp.tool()(oxigraph_create_quad)
    mcp.tool()(oxigraph_add)
    mcp.tool()(oxigraph_add_many)
    mcp.tool()(oxigraph_remove)
    mcp.tool()(oxigraph_remove_many)
    mcp.tool()(oxigraph_clear)
    mcp.tool()(oxigraph_quads_for_pattern)
    
    mcp.tool()(oxigraph_query)
    mcp.tool()(oxigraph_update)
    mcp.tool()(oxigraph_query_with_options)
    mcp.tool()(oxigraph_prepare_query)
    mcp.tool()(oxigraph_execute_prepared_query)
    mcp.tool()(oxigraph_run_query)
    
    mcp.tool()(oxigraph_parse)
    mcp.tool()(oxigraph_serialize)
    mcp.tool()(oxigraph_import_file)
    mcp.tool()(oxigraph_export_graph)
    mcp.tool()(oxigraph_get_supported_formats)
    
    # Start with SSE transport
    logger.info("Starting SSE server on http://localhost:8000")
    mcp.run(transport='sse')

if __name__ == "__main__":
    main()