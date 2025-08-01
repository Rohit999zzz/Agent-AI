import requests
import os
from langchain.tools import Tool

def create_web_search_tool():
    def search_web(query):
        """Search the web using SerpAPI"""
        try:
            params = {
                'q': query,
                'api_key': os.getenv('SERPAPI_API_KEY'),
                'engine': 'google',
                'num': 5
            }
            
            response = requests.get('https://serpapi.com/search', params=params)
            results = response.json()
            
            if 'organic_results' in results:
                search_results = []
                for result in results['organic_results'][:3]:
                    search_results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', '')
                    })
                
                formatted_results = "\n".join([
                    f"Title: {r['title']}\nSummary: {r['snippet']}\nURL: {r['link']}\n"
                    for r in search_results
                ])
                
                return f"Web search results for '{query}':\n\n{formatted_results}"
            else:
                return "No search results found."
                
        except Exception as e:
            return f"Error searching web: {str(e)}"
    
    return Tool(
        name="WebSearch",
        description="Search the internet for current information. Use this when you need up-to-date information or facts not in your knowledge base.",
        func=search_web
    ) 