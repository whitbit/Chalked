
import scrapy
import re

# move the functions outside and states dictionaries

class QuotesSpider(scrapy.Spider):
    
    name = "route_search"


    popular_states = {

        'alabama': '105905173',
        'arizona': '105708962',
        'california': '105708959',
        'colorado': '105708956', 
        'nevada': '105708961',        
        'new hampshire': '105872225',
        'utah': '105708957',
        'wisconsin': '105708968',
        'texas': '105835804',
    }

    other_states = {     
 
        'arkansas': '105901027',
        'connecticut' : '105806977',
        'hawaii': '106316122',
        'illinois': '105911816',
        'maryland': '106029417',
        'massachusetts': '105908062',
        'minnesotta': '105812481',
        'new_mexico': '105708964',
        'new_york': '105800424',
        'oregon': '105708965',
        'penn': '105913279',
        'sd': '105708963',
        'tenn': '105887760',
        'virginia': '105852400',
        'west_v': '105855459',
        'wyoming': '105708960',
    }


    def start_requests(self):


        def get_one_pg_results(other_states):
            
            urls = []
            
            for state in other_states:

                urls.append('https://www.mountainproject.com/scripts/Search.php?searchType=routeFinder&minVotes=10&selectedIds=%27' 
                            + other_states[state]
                            + '%27&type=boulder&diffMinrock=1800&diffMinboulder=20000&diffMinaid=70000&diffMinice=30000&diffMinmixed=50000&diffMaxrock=5500&diffMaxboulder=21400&diffMaxaid=75260&diffMaxice=38500&diffMaxmixed=60000&is_trad_climb=1&is_sport_climb=1&is_top_rope=1&stars=0&pitches=0&sort1=area&sort2=rating')

            return urls


        def get_multiple_pg_results(popular_states):
            
            urls = []
            
            for state in popular_states:

                first_page = ('https://www.mountainproject.com/scripts/Search.php?searchType=routeFinder&minVotes=10&selectedIds=%27' 
                            + popular_states[state]
                            + '%27&type=boulder&diffMinrock=1800&diffMinboulder=20000&diffMinaid=70000&diffMinice=30000&diffMinmixed=50000&diffMaxrock=5500&diffMaxboulder=21400&diffMaxaid=75260&diffMaxice=38500&diffMaxmixed=60000&is_trad_climb=1&is_sport_climb=1&is_top_rope=1&stars=0&pitches=0&sort1=area&sort2=rating')


                urls.append(first_page)
                
                for i in range(2,21):
                    urls.append(first_page[:] + '&page=' + str(i))
            
            return urls

        
        urls = get_one_pg_results(self.other_states)
        urls.extend(get_multiple_pg_results(self.popular_states))


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        num_pattern = re.compile("\w*\/(\d+)")
        samples = response.css('td p a:first-child').extract()
        nums = set([( sample, num_pattern.search(sample).group(1).encode('ascii')) 
                   for sample in samples if num_pattern.search(sample) 
                   and len(num_pattern.search(sample).group(1))==9])
        
        results = {}
        
        for url, num in nums:
            results[url] = num
        return results

