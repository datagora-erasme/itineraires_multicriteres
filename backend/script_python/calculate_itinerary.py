import sys
import concurrent.futures
from calculate_itinerary_utils import shortest_path

startLat = float(sys.argv[1])
startLon = float(sys.argv[2])

endLat = float(sys.argv[3])
endLon = float(sys.argv[4])

pathLength = sys.argv[5]
pathIf = sys.argv[6]

start = (startLat, startLon)
end = (endLat, endLon)

# print(start, end)
# temp_path = "./temp/temp_sp.json"
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(shortest_path("./data/osm/final_network.gpkg", pathLength, origin_point=start, destination_point=end, weight="length"))
    executor.submit(shortest_path("./data/osm/final_network.gpkg", pathIf, origin_point=start, destination_point=end, weight="IF"))

print(pathLength)
print(pathIf)

sys.stdout.flush()