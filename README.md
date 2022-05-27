# The-Bus-Problem-SO2

### This project is a tribute to MPK Wrocław, their very reliable trams and their ticket inspectors. I hope that all my fines helped them improve their living.

<img src="252760_252628.png">

## Description of the problem
People come to the bus stop, buy a ticket, and wait for a bus that can take 𝑁 people. When the bus arrives, the waiting people get on the bus, but if someone came while getting on, they have to wait for the next bus. People must also wait for the next bus if there are more than 𝑁 people waiting. When all the people waiting get on the bus, the bus can leave. If there is no one at the bus stop then the bus will leave immediately. Some people may try to get on the bus without a ticket (e.g. 5% of the people) so sometimes there will be a ticket control at the entrance of the bus (e.g. 10% of the trips), in this case people without a ticket will not be allowed on.

## Threads and resources
Threads: bus, people waiting.
Resources: seats on the bus.

## Critical sections
The critical sections will be getting on the right bus (one of the three bus lines), and buying a ticket.

## Where will conditional variables be used?
Conditional variables will be used to:
- notifying those waiting that one person among them can get on and only when the bus of the right line,
- to tell the next person to buy a ticket,
- notify that the next person can proceed to ticket control.

## Where can deadlocks and jams occur in case of bad 
implementation?
- It may be that no one ever gets on the bus.
- It may turn out that the bus never arrives.
- It may turn out that no one ever buys a ticket.
- It may turn out that ticket control will stop the bus forever.
