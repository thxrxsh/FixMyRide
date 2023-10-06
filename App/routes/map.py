from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from geopy.distance import geodesic
import requests
import models, schemas, utils, database, oauth2
from database import get_db
from config import Settings


router = APIRouter(prefix='/map', tags=['Map'])


@router.get('/', status_code=status.HTTP_200_OK)
def getDefaultMap(filter_data: schemas.MapFilter, db: Session = Depends(get_db)):
    
    if (filter_data.filter_type == 'country'):
        mechanics = (
                    db.query(models.Mechanic)
                        .filter(models.Mechanic.country == filter_data.country)
                        .with_entities(
                            models.Mechanic.mechanic_id,
                            models.Mechanic.address,
                            models.Mechanic.location,
                            models.Mechanic.mobile,
                            models.Mechanic.name,
                            ( func.coalesce(models.Mechanic.rating_count / models.Mechanic.rating_total * 5, 0)).label("rating")    
                        )
                        .all()
                    )


    elif (filter_data.filter_type == 'province'):
        mechanics = (
                    db.query(models.Mechanic)
                        .filter(models.Mechanic.province == filter_data.province)
                        .with_entities(
                            models.Mechanic.mechanic_id,
                            models.Mechanic.address,
                            models.Mechanic.location,
                            models.Mechanic.mobile,
                            models.Mechanic.name,
                            ( func.coalesce(models.Mechanic.rating_count / models.Mechanic.rating_total * 5, 0)).label("rating")    
                        )
                        .all()
                    )
                    

    elif (filter_data.filter_type == 'district'):
        mechanics = (
                    db.query(models.Mechanic)
                        .filter(models.Mechanic.district == filter_data.district)
                        .with_entities(
                            models.Mechanic.mechanic_id,
                            models.Mechanic.address,
                            models.Mechanic.location,
                            models.Mechanic.mobile,
                            models.Mechanic.name,
                            ( func.coalesce(models.Mechanic.rating_count / models.Mechanic.rating_total * 5, 0)).label("rating")    
                        )
                        .all()
                    )

    mechanic_data = [
        {
            "mechanic_id": mechanic.mechanic_id,
            "address": mechanic.address,
            "location": mechanic.location,
            "mobile": mechanic.mobile,
            "name": mechanic.name,
            "rating": mechanic.rating
        }
        for mechanic in mechanics
    ]

    return mechanic_data




@router.get('/nearest', status_code=status.HTTP_200_OK)
def getNearest(filter_data: schemas.MapFilter, db: Session = Depends(get_db)):
    
    # data = db.query(models.Mechanic.mechanic_id,models.Mechanic.location).filter(models.Mechanic.country == filter_data.country).all()
    
    query = db.query(models.Mechanic)

    # Filter by country
    query = query.filter(models.Mechanic.country == filter_data.country)

    # Filter by vehicle type (assuming filter_data.vehicle_type is provided)
    if filter_data.vehicle_type:
        query = query.join(models.Service, isouter=False)  # Join Service table using INNER JOIN
        query = query.filter(models.Service.vehicle_type == filter_data.vehicle_type)

    # Filter by vehicle model (assuming filter_data.model is provided)
    if filter_data.model:
        query = query.filter(models.Service.model == filter_data.model)

    # Filter by service (assuming filter_data.service is provided)
    if filter_data.service:
        service_pattern = f"%{filter_data.service}%"  # Add '%' wildcards for partial match
        query = query.filter(models.Service.service.like(service_pattern))

    # Select relevant columns
    query = query.with_entities(
        models.Mechanic.mechanic_id,
        models.Mechanic.location,
    )

    data = query.all()

    if data:

        mechanic_coordinates = [ (mechanic[0], tuple(map(float, mechanic[1].split(',')))) for mechanic in data ]

        user_coordinate = tuple(map(float, filter_data.location.split(','))) 

        mechanics_filterd_by_displacement = utils.filter_by_radius(radius=filter_data.radius, origin=user_coordinate, mechanic_coordinates=mechanic_coordinates)

        mechanics_with_distances = [(mechanic[0] ,mechanic[1], utils.calculate_road_distance(user_coordinate, mechanic[1])) for mechanic in mechanics_filterd_by_displacement]
        
        if mechanics_with_distances:
            sorted_mechanic_locations = sorted(mechanics_with_distances, key=lambda x: x[2])
            return sorted_mechanic_locations

    return {}