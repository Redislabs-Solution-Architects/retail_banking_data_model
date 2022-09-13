package com.bestarch.demo.runner;

import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import com.bestarch.demo.domain.Customer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.redis.lettucemod.api.StatefulRedisModulesConnection;
import com.redis.lettucemod.api.sync.RediSearchCommands;
import com.redis.lettucemod.search.Document;
import com.redis.lettucemod.search.SearchResults;

@Component
@Order(1)
public class CustomerRunner implements CommandLineRunner {
	
	private static Logger logger = LoggerFactory.getLogger(CustomerRunner.class);
	
	@Autowired
	private StatefulRedisModulesConnection<String, String> connection;
	
	private final static ObjectMapper objectMapper = new ObjectMapper();
	
	/**
	 * Actual RediSearch query --> 
	 * FT.SEARCH idx_customer '@email:(tiwarimishti\@example.org)'
	 */
	private final static String CUSTOMER_BY_EMAIL = "@email:(tiwarimishti\\@example.org)";
	
	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		
		SearchResults<String, String> results = commands.ftSearch("idx_customer", CUSTOMER_BY_EMAIL);
		
		logger.info("*********** Get customer by email *******************");
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
		logger.info("***********************************************************\n");
	}

}
