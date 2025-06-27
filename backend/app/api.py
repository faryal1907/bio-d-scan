from fastapi import APIRouter, HTTPException
from typing import List
from app.models import BeeDataCreate, BeeDataResponse
from app.database import bee_data_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/api/bee-data", response_model=BeeDataResponse, status_code=201)
async def add_bee_data(data: BeeDataCreate):
    """Add new bee data to the database"""
    try:
        data_dict = data.dict()
        data_dict["timestamp"] = datetime.now()
        
        result = await bee_data_collection.insert_one(data_dict)
        
        # Get the inserted document
        inserted_data = await bee_data_collection.find_one({"_id": result.inserted_id})
        inserted_data["id"] = str(inserted_data.pop("_id"))
        
        return BeeDataResponse(**inserted_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add bee data: {str(e)}")

@router.get("/api/bee-data", response_model=List[BeeDataResponse])
async def get_bee_data(limit: int = 1000):
    """Get bee data with optional limit"""
    try:
        cursor = bee_data_collection.find({}).sort("timestamp", -1).limit(limit)
        data = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            data.append(BeeDataResponse(**document))
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch bee data: {str(e)}")

@router.get("/api/bee-data/{hive_id}")
async def get_bee_data_by_hive(hive_id: str):
    """Get bee data for a specific hive"""
    try:
        cursor = bee_data_collection.find({"hive_id": hive_id}).sort("timestamp", -1)
        data = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            data.append(document)
        return {"hive_id": hive_id, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch hive data: {str(e)}")

@router.delete("/api/bee-data/{data_id}")
async def delete_bee_data(data_id: str):
    """Delete bee data by ID"""
    try:
        result = await bee_data_collection.delete_one({"_id": ObjectId(data_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete data: {str(e)}")

@router.get("/api/stats")
async def get_stats():
    """Get statistics about bee data"""
    try:
        total_count = await bee_data_collection.count_documents({})
        
        # Get average temperature and humidity
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_temperature": {"$avg": "$temperature"},
                    "avg_humidity": {"$avg": "$humidity"},
                    "min_temperature": {"$min": "$temperature"},
                    "max_temperature": {"$max": "$temperature"}
                }
            }
        ]
        
        stats = await bee_data_collection.aggregate(pipeline).to_list(1)
        
        return {
            "total_records": total_count,
            "averages": stats[0] if stats else {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")