# Variables and Includes Example
create workout "Advanced Split"
set goal "Strength and Conditioning"

let rest_time = 45
let set_count = 4

include "warmup.dsl"

add exercise "deadlifts" for set_count sets of 5
rest rest_time seconds
add exercise "bench press" for set_count sets of 6
rest rest_time seconds
add exercise "rows" for set_count sets of 8

repeat Monday, Thursday
save workout