from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import FlowchartInstanceModel, AugmentModel, RequestAugmentValues


router = APIRouter()

@router.post("/flowchart",response_description="Create Flowchart instance.")
async def create_flowchart(request: Request,flowchart: FlowchartInstanceModel = Body(...)):
    flowchart = jsonable_encoder(flowchart)
    new_flowchart = await request.app.mongodb["flowcharts"].insert_one(flowchart)
    created_flowchart = await request.app.mongodb["flowcharts"].find_one(
        {"_id":new_flowchart.inserted_id}
    )
    print("created_flowchart in monogdb:",new_flowchart)

    return JSONResponse(status_code = status.HTTP_201_CREATED,content=created_flowchart)

@router.post("/augment",response_description="Create Augment entry in database.")
async def create_augment(request: Request,augment: AugmentModel = Body(...)):
    augment = jsonable_encoder(augment)
    new_augment = await request.app.mongodb["augment_basic_info"].insert_one(augment)
    created_augment = await request.app.mongodb["augment_basic_info"].find_one(
        {"_id":new_augment.inserted_id}
    )
    #print("created_flowchart in monogdb:",new_augment)

    return JSONResponse(status_code = status.HTTP_201_CREATED,content=created_augment)

@router.get("/augments/tier/{tier}",response_description="Get all augments of certain tier in db.")
async def get_all_augments_of_tier(tier: int,request: Request):
    augments = []
    for doc in await request.app.mongodb["augment_basic_info"].find(filter={'tier':tier}).to_list(length=100):
        augments.append(doc)
    if len(augments) == 0:
        raise HTTPException(status_code=404,detail=f"ERROR: No augments in DB.")
    return augments

@router.get("/flowcharts",response_description="Get all active Flowchart instances.")
async def get_flowcharts(request: Request):
    flowcharts = []
    for doc in await request.app.mongodb["flowcharts"].find().to_list(length=100):
        flowcharts.append(doc)
    return flowcharts


@router.get("/augments/match/{tier}",response_description="Get all active Flowchart instances that have the best matches based on given input.")
async def get_augment_based_on_value_match_and_tier(request: Request,tier: int, incoming_values: RequestAugmentValues= Body(...)):
    #minimum requirement is a tier, to go off of
    values = jsonable_encoder(incoming_values)
    print('incoming values:',values)

    augments = []
    for doc in await request.app.mongodb["augment_basic_info"].find(filter={'tier':tier}).to_list(length=100):
        augments.append(doc)
    if len(augments) == 0:
        raise HTTPException(status_code=404,detail=f"ERROR: No augments in DB.")

    
    #find all augments that have a shared values
    res = []
    for augment in augments:
        #print('array1',values['values'])
        #print('array2',augment['data_values'].keys())
        combined = set()

        for value in values['values']:
            if value in augment['data_values'].keys():
                combined.add(value)
        
        if len(combined) !=0:
            print('name',augment['name'])
            print('shared values:',combined)

    return augments


@router.get("/augments",response_description="Get all possible augments.")
async def get_augments(request: Request):
    augments = []
    for doc in await request.app.mongodb["augment_basic_info"].find().to_list(length=100):
        augments.append(doc)
    if len(augments) == 0:
        raise HTTPException(status_code=404,detail=f"ERROR: No augments in DB.")
    return augments

@router.get("/flowcharts/{flow_chart_id}",response_description="Get a single Flowchart instance.")
async def get_single_flowchart(flow_chart_id: str, request: Request):
    if (flowchart := await request.app.mongodb["flowcharts"].find_one({"_id":flow_chart_id})) is not None:
        return flowchart 
    
    raise HTTPException(status_code=404,detail=f"Task {id} not found.")

@router.put("/{id}",response_description="Update a Flowchart instance by id.")
async def update_task(id: str, request: Request, flowchart: FlowchartInstanceModel = Body(...)):
    flowchart = {k: v for k, v in flowchart.dict().items() if v is not None}

    if len(flowchart) >=1:
        update_result = await request.app.mongodb["flowcharts"].update_one(
            {"_id": id}, {"$set":flowchart}
        )

        if update_result.modified_count == 1:
            if (
                updated_flowchart := await request.app.mongodb["flowcharts"].find_one({"_id":id})
            ) is not None:
                return updated_flowchart
    
    if (
        existing_flowchart := await request.app.mongodb["flowcharts"].find_one({"_id":id})
    ) is not None:
        return existing_flowchart 

    raise HTTPException(status_code = 404, detail=f"Task {id} not found")

@router.delete("/{id}", response_description="Delete Flowchart instance.")
async def delete_flowchart(id: str, request: Request):
    delete_result = await request.app.mongodb["flowcharts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404,detail=f"Flowchart {id} not found.")