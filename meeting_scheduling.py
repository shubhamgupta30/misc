
def getTimeStamps (meetings):
  time_stamps = []
  for meeting in meetings:
    time_stamps.append((meeting, "start", meeting[0]))
    time_stamps.append((meeting, "end", meeting[1]))
  return sorted(time_stamps, key=lambda time_stamp: time_stamp[2])

# Assuming sane input i.e. there is no meeting whose start and end time are
# such that start_time >= end_time.
def allocate_rooms(meetings):
  ## Setting up rooms
  free_rooms = []
  next_free = 0
  meeting_to_room = {}
  room_to_meeting = {}
  def free_room(meeting):
    free_rooms.append(meeting_to_room[meeting])
    del meeting_to_room[meeting]
  def allocate_room(meeting):
    nonlocal next_free
    if len(free_rooms) == 0:
      allocated_room = next_free
      next_free += 1
    else:
      allocated_room = free_rooms.pop()
    room_to_meeting.setdefault(allocated_room, [])
    room_to_meeting[allocated_room].append(meeting)
    meeting_to_room[meeting] = allocated_room 

  ## Perform allocation
  time_stamps = getTimeStamps(meetings)
  for (meeting, description, t) in time_stamps:
    if (description == "end"):
      free_room(meeting)
    else:
      allocate_room(meeting)

  ## Report the allocation
  print ("meetings: ", meetings)
  for (room, meetings) in room_to_meeting.items():
    for meeting in meetings:
      print ('Room number %d hosts meeting (%d, %d)' % (room, meeting[0], meeting[1]))

if __name__ == "__main__":
  allocate_rooms([(1,5), (2,6), (3,7),(4,8),(5,9), (6,10)])
    
