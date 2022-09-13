package com.bestarch.demo.runner;

import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import com.redis.lettucemod.api.StatefulRedisModulesConnection;
import com.redis.lettucemod.api.sync.RediSearchCommands;
import com.redis.lettucemod.search.AggregateOptions;
import com.redis.lettucemod.search.AggregateResults;
import com.redis.lettucemod.search.Document;
import com.redis.lettucemod.search.Group;
import com.redis.lettucemod.search.Reducers;
import com.redis.lettucemod.search.Reducers.Count;
import com.redis.lettucemod.search.SearchOptions;
import com.redis.lettucemod.search.SearchResults;

@Component
@Order(2)
public class CreditCardRunner implements CommandLineRunner {
	
	private static Logger logger = LoggerFactory.getLogger(CreditCardRunner.class);

	@Autowired
	private StatefulRedisModulesConnection<String, String> connection;

	/**
	 * Actual RediSearch query --> 
	 * FT.SEARCH idx_cccard '@cif:(QEOE110093342)' return 2 creditCardNo type
	 */
	private final static String CREDIT_CARD_BY_CIF = "@cif:(QEOE110093342)";
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_cccard * groupby 1 @type REDUCE COUNT 0 as ccTypes
	 */
	private final static String TOTAL_NO_OF_CC_BY_TYPE = "*";
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_cccard '@active:{false}' groupby 1 @active REDUCE COUNT 0 as inactiveCards
	 */
	private final static String TOTAL_NO_OF_INACTIVE_CC = "@active:{false}";

	@Override
	public void run(String... args) throws Exception {
		getAllCreditCardByCIF();
		getTotalNoOfCCByType();
		getTotalNoOfInactiveCC();
	}

	private void getAllCreditCardByCIF() {
		RediSearchCommands<String, String> commands = connection.sync();
		SearchOptions<String, String> searchOptions = SearchOptions.<String, String>builder()
				.returnFields(new String[] { "creditCardNo", "type" })
				.build();
		
		SearchResults<String, String> results = commands.ftSearch("idx_cccard", CREDIT_CARD_BY_CIF, searchOptions);
		
		logger.info("*********** Credit cards by CIF *******************");
		for (Document<String, String> doc : results) {
			Set<Entry<String, String>> entrySet = doc.entrySet();
			Iterator<Entry<String, String>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, String> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		logger.info("***********************************************************\n");
	}
	
	private void getTotalNoOfCCByType() {
		RediSearchCommands<String, String> commands = connection.sync();
		Count countReducer = Reducers.Count.as("ccTypes");
				
		Group group = Group
				.by(new String[] { "type" })
				.reducer(countReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_cccard", TOTAL_NO_OF_CC_BY_TYPE, aggregateOptions);
		
		logger.info("*********** Total no of credit card by type *******************");
		for (Map<String, Object> map : results) {
			Set<Entry<String, Object>> entrySet = map.entrySet();
			Iterator<Entry<String, Object>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, Object> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		logger.info("***********************************************************\n");
	}
	
	
	private void getTotalNoOfInactiveCC() {
		RediSearchCommands<String, String> commands = connection.sync();
		Count countReducer = Reducers.Count.as("inactiveCards");
				
		Group group = Group
				.by(new String[] { "active" })
				.reducer(countReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_cccard", TOTAL_NO_OF_INACTIVE_CC, aggregateOptions);
		
		logger.info("*********** Total no of inactive credit cards *******************");
		for (Map<String, Object> map : results) {
			Set<Entry<String, Object>> entrySet = map.entrySet();
			Iterator<Entry<String, Object>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, Object> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		logger.info("***********************************************************\n");
	}

}
