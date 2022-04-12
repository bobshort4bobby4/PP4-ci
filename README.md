# **ROOM BOOKING APP**

(CTRL + Click to open links in new window)

The deployed site can be found [here](https://PP4-CI.herokuapp.com/)

Github repository can be accessed [here](https://github.com/bobshort4bobby4/pp4-CI)


MOCKUP TOGO HERE




# **Introduction**

This is the fourth project I have completed as part of the[Code Institute Full Stack Diploma Course](https://codeinstitute.net).  

The project sets out to create a website for a fictitious hotel.  Rooms can be booked and cancelled via the site, as well as extended if availability exsists for that room,  if the  current room is booked  another room of the same type will be suggested if available.  
The room should only be cancelled if the check in date is not more the 48 hours away.

The imaginery product owner has also requested that rooms are put on sale if occupancy drops below a set percentage.  
She also requested a review section where customers could leave feedback on their stay at the hotel and email confirmation for all customer interactions.
  
# User Experience/User Interface (UX/UI)

<details>  
            
<summary>User Experience/User Interface (UX/UI)</summary>    
  
  
  
   
  
The AGIILE methodology for project development will be used to produce this project, this method involves continual collaboration between all parties and improvments   at every stage. It helps to ensure good quality products are produced within time and financial constraints.
  
   ### User Stories  
  
   #### Casual Visitor Goals
   As a Casual Visitor I want:
  - to be easily able to ascertain information on the hotel and it's locality to aid my purchasing decision.
  - to be able to check availability for my room choice on any particular set of dates to aid my purchasing decision.
  - to navigate easily around the site to avoid frustration whilst using the site and to engender positive emotions towards the business.
  - to have any incorrect input rejected and the error explained clearly and quickly so I do not have any frustrating emotions using the site. 
    
  #### Customer Goals
  As a Customer I want:
  - to be able to easily book a room.
  - to be able to easily cancel a booking if there is more than 48 hours to check in to manage my booking.
  - to be able to easly extend my stay if possible to manage my booking .
  - to be easily able to view my booking and account details to make using the site as easy as possible.
  - to be easily able to change account details to make use as easy as possible.
  - to have all actions confirmed to me so as to avoid any confusion or mis-understandings.
  - to be able to leave a review of the hotel to improve my experience using the site/business.  
    
  #### Site Owner/Administrator
  As a Site Owner/Administrator I want:
  - to be able to view bookings to enable proper planning.
  - to be able to view/change rooms to keep room inventory current.
  - to be able to view customer information to enable efficient communication.
  - to provide a quality website in order to drive sales and increase profits.
  
  
  Using the user stories as a frame of reference the following Epics were formulated;
  
  - implement basic html and django structure
  - implement user registration and login
  - implement room booking management system
  - implement user feedback system
  - optimise the django admin panel to aid hotel management functions.
  
  The user stories were prioritised using the MoSCoW technique and the Kanban Board feature built-in to Github will be used as an information radiator.
  The user stories were broken down into tasks and these were listed under their respective Epic in the initial Kanban Board/
  Care was taken to ensure should-have proioritised user stories are not greater than 60% of the total.
  
  ### Wireframes
  
  
  
  ### Database Relations
  
  After normalization I used the following data base schema.
  RoomType
  type: charfield
  description: textfield
  price: decimalfield
  Max occupants: integerfield
  
  
  Room:
  room-number:integer
  type:foregin to roomtype
  Booked:boolean
  occupied:boolean
  
  Booking:
  user:foregin to user oath
  roomm-number: foregin to Room
  checkin: datefield
  checkout:date field
  isactive: boolean
  
  
  
  
  
  
</details>
