package com.bestarch.demo.service;

import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import com.bestarch.demo.domain.Customer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.redislabs.lettusearch.Document;
import com.redislabs.lettusearch.RediSearchCommands;
import com.redislabs.lettusearch.SearchOptions;
import com.redislabs.lettusearch.SearchResults;
import com.redislabs.lettusearch.StatefulRediSearchConnection;

@Component
@Order(1)
public class CustomerRunner implements CommandLineRunner {
	
	@Autowired
	private StatefulRediSearchConnection<String, String> connection;
	
	private final static ObjectMapper objectMapper = new ObjectMapper();
	
	//FT.SEARCH idx_customer '@email:(tiwarimishti\@example.org)'
	private final static String QUERY = "@email:(tiwarimishti\\@example.org)";
	
	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		//SortBy<String> sortBy = SortBy.<String>builder().field("productName").build();
		//Limit limit = SearchOptions.Limit.builder().offset(offset).num(page).build();
		SearchOptions<String> searchOptions = SearchOptions
				.<String>builder()
				//.sortBy(sortBy)
				//.limit(limit)
				.build();
		SearchResults<String, String> results = commands.search("idx_customer", QUERY);
		
		Customer c = null;
		for (Document<String, String> doc : results) {
			Set<Entry<String, String>> entrySet = doc.entrySet();
			Iterator<Entry<String, String>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, String> en = iter.next();
				if ("$".equals(en.getKey())) {
					try {
						c = objectMapper.readValue(en.getValue(), Customer.class);
						System.out.println("Searched record:: " + c);
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}
		}
		System.out.println("********************************************************************************************");
	}

}
