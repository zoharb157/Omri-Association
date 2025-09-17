#!/usr/bin/env python3
"""
FastAPI Backend for Omri Association Dashboard
Provides REST API endpoints for frontend consumption
"""

import logging
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import existing modules
from data_processing import (
    calculate_donor_statistics,
    calculate_monthly_budget,
    calculate_widow_statistics,
)
from google_sheets_io import read_sheet, read_widow_support_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Omri Association API",
    description="REST API for Omri Association Dashboard",
    version="1.0.0",
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data cache
data_cache = {}
cache_timestamp = None
CACHE_DURATION = 300  # 5 minutes


def get_cached_data():
    """Get data from cache or load fresh data"""
    global data_cache, cache_timestamp
    import time

    current_time = time.time()

    # Return cached data if it's still fresh
    if cache_timestamp and (current_time - cache_timestamp) < CACHE_DURATION:
        return data_cache

    try:
        logger.info("Loading fresh data from Google Sheets...")

        # Load all data
        expenses_df = read_sheet("Expenses")
        donations_df = read_sheet("Donations")
        almanot_df = read_widow_support_data()
        investors_df = read_sheet("Investors")

        # Process data
        budget_status = calculate_monthly_budget(expenses_df, donations_df)
        donor_stats = calculate_donor_statistics(donations_df)
        widow_stats = calculate_widow_statistics(almanot_df)
        # TODO: Add network data processing
        network_data = {}

        # Cache the data
        data_cache = {
            "expenses": expenses_df.to_dict("records") if expenses_df is not None else [],
            "donations": donations_df.to_dict("records") if donations_df is not None else [],
            "almanot": almanot_df.to_dict("records") if almanot_df is not None else [],
            "investors": investors_df.to_dict("records") if investors_df is not None else [],
            "budget_status": budget_status,
            "donor_stats": donor_stats,
            "widow_stats": widow_stats,
            "network_data": network_data,
        }

        cache_timestamp = current_time
        logger.info("Data loaded and cached successfully")

        return data_cache

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}") from e


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Omri Association API is running", "status": "healthy"}


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    try:
        data = get_cached_data()
        return {
            "status": "healthy",
            "data_loaded": True,
            "cache_timestamp": cache_timestamp,
            "record_counts": {
                "expenses": len(data.get("expenses", [])),
                "donations": len(data.get("donations", [])),
                "almanot": len(data.get("almanot", [])),
                "investors": len(data.get("investors", [])),
            },
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """Get dashboard overview data"""
    try:
        data = get_cached_data()
        return {
            "budget_status": data["budget_status"],
            "donor_stats": data["donor_stats"],
            "widow_stats": data["widow_stats"],
        }
    except Exception as e:
        logger.error(f"Error getting dashboard overview: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/data/expenses")
async def get_expenses():
    """Get expenses data"""
    try:
        data = get_cached_data()
        return {"expenses": data["expenses"]}
    except Exception as e:
        logger.error(f"Error getting expenses: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/data/donations")
async def get_donations():
    """Get donations data"""
    try:
        data = get_cached_data()
        return {"donations": data["donations"]}
    except Exception as e:
        logger.error(f"Error getting donations: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/data/almanot")
async def get_almanot():
    """Get almanot (widows) data"""
    try:
        data = get_cached_data()
        return {"almanot": data["almanot"]}
    except Exception as e:
        logger.error(f"Error getting almanot: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/data/investors")
async def get_investors():
    """Get investors data"""
    try:
        data = get_cached_data()
        return {"investors": data["investors"]}
    except Exception as e:
        logger.error(f"Error getting investors: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/network")
async def get_network_data():
    """Get network visualization data"""
    try:
        data = get_cached_data()
        return {"network_data": data["network_data"]}
    except Exception as e:
        logger.error(f"Error getting network data: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/api/reports/monthly")
async def get_monthly_report():
    """Get monthly report data"""
    try:
        data = get_cached_data()
        # This would include processed monthly report data
        return {
            "monthly_data": {
                "expenses": data["expenses"],
                "donations": data["donations"],
                "summary": data["budget_status"],
            }
        }
    except Exception as e:
        logger.error(f"Error getting monthly report: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
