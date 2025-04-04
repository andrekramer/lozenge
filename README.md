Lozenge is a common symbol in neolythic art such as at Brú na Bóinne.  

Add api keys to files called model-api-key e.g. gemini-api-key for models you initend to use.   

To install:   
source py-install   

To run:   
python prog.py   

Lozenge aims to support a dialectic form of reasoning.   

Put some thesis or prior synthesis into a file called synthesis and run:    
python dialectrician.py    
(the synthesis is saved so you can itterate if SYNTHESIS_ONLY=True)   

Install as an MCP (Model Context Protocol) server:    
mcp install dialectic_server.py     

Make sure you add aiohttp as a dependency (see claud_desktop_config.json for claud desktop)   
(add the install location as FILEPATH in support.py or set as an env var in claud_desktop_config.json file)     

