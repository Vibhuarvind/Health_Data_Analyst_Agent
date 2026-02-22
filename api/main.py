"""FastAPI REST API for Health Data Analyst.

This module provides a production-ready REST API with:
- Query endpoint for natural language health data analysis
- Health check endpoint
- Request/response validation with Pydantic
- Error handling and logging
"""
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
from src.core.pipeline import HealthDataPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Health Data Analyst API",
    description="GenAI-powered health data analysis via natural language queries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline (singleton pattern)
pipeline = HealthDataPipeline()


# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    """Request model for health data queries."""
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Natural language question about health data",
        example="What is the average BMI of patients with chronic kidney disease?"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging for debugging"
    )


class QueryResponse(BaseModel):
    """Response model for query results."""
    question: str = Field(..., description="Original query")
    status: str = Field(..., description="Execution status: 'success' or 'failed'")
    answer: Optional[str] = Field(None, description="Natural language answer")
    generated_code: Optional[str] = Field(None, description="Generated Python/Pandas code")
    execution_time_ms: float = Field(..., description="Total execution time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if query failed")


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    service: str
    version: str


# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "service": "Health Data Analyst API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint for monitoring.
    
    Returns:
        HealthCheckResponse with service status
    """
    logger.info("Health check requested")
    return HealthCheckResponse(
        status="healthy",
        service="health-data-analyst",
        version="1.0.0"
    )


@app.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_health_data(request: QueryRequest) -> QueryResponse:
    """
    Execute a natural language query on health data.
    
    This endpoint:
    1. Generates Python/Pandas code from natural language
    2. Validates code for security
    3. Executes code on health datasets
    4. Returns natural language insights
    
    Args:
        request: QueryRequest with question and optional verbose flag
        
    Returns:
        QueryResponse with answer, generated code, and execution metrics
        
    Raises:
        HTTPException: If query execution fails
    """
    logger.info(f"Processing query: {request.question}")
    
    try:
        # Run pipeline
        result = pipeline.run(request.question, verbose=request.verbose)
        
        # Check if execution was successful
        if result["status"] != "success":
            logger.error(f"Query failed: {result.get('error')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": result.get("error", "Unknown error"),
                    "question": request.question
                }
            )
        
        # Build successful response
        response = QueryResponse(
            question=result["question"],
            status=result["status"],
            answer=result["final_response"],
            generated_code=result["py_code"],
            execution_time_ms=result["timings_ms"]["total"],
            error=None
        )
        
        logger.info(f"Query successful in {result['timings_ms']['total']:.2f}ms")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": f"Internal server error: {str(e)}",
                "question": request.question
            }
        )


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get system metrics (placeholder for production monitoring).
    
    Returns:
        Dictionary with basic metrics
    """
    return {
        "service": "health-data-analyst",
        "status": "operational",
        "endpoints": {
            "query": "/query",
            "health": "/health",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
