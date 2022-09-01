package com.bestarch.demo.runner;

import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import com.redislabs.lettusearch.AggregateOptions;
import com.redislabs.lettusearch.AggregateOptions.Operation.GroupBy.Reducer;
import com.redislabs.lettusearch.AggregateOptions.Operation.GroupBy.Reducer.Count;
import com.redislabs.lettusearch.AggregateResults;
import com.redislabs.lettusearch.Document;
import com.redislabs.lettusearch.RediSearchCommands;
import com.redislabs.lettusearch.SearchOptions;
import com.redislabs.lettusearch.SearchResults;
import com.redislabs.lettusearch.StatefulRediSearchConnection;

@Component
@Order(2)
public class CreditCardRunner implements CommandLineRunner {

	@Autowired
	private StatefulRediSearchConnection<String, String> connection;

	// FT.SEARCH idx_cccard '@cif:(QEOE110093342)' return 2 creditCardNo type
	private final static String CREDIT_CARD_BY_CIF = "@cif:(QEOE110093342)";
	
	//FT.AGGREGATE idx_cccard * groupby 1 @type REDUCE COUNT 0 as ccTypes
	private final static String TOTAL_NO_OF_CC_BY_TYPE = "*";
	
	//FT.AGGREGATE idx_cccard '@active:{false}' groupby 1 @active REDUCE COUNT 0 as inactiveCards
	private final static String TOTAL_NO_OF_INACTIVE_CC = "@active:{false}";

	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		getAllCreditCardByCIF(commands);
		getTotalNoOfCCByType(commands);
		getTotalNoOfInactiveCC(commands);
	}

	private void getAllCreditCardByCIF(RediSearchCommands<String, String> commands) {
		SearchOptions<String> searchOptions = SearchOptions.<String>builder()
				.returnFields(Arrays.asList(new String[] { "creditCardNo", "type" })).build();
		
		SearchResults<String, String> results = commands.search("idx_cccard", CREDIT_CARD_BY_CIF, searchOptions);
		
		System.out.println("*********** Credit cards by CIF *******************");
		for (Document<String, String> doc : results) {
			Set<Entry<String, String>> entrySet = doc.entrySet();
			Iterator<Entry<String, String>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, String> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		System.out.println("********************************************************************************************\n");
	}
	
	private void getTotalNoOfCCByType(RediSearchCommands<String, String> commands) {
		Collection<String> groupByField = Arrays.asList(new String[] { "type" });
		Count countReducer = Reducer.Count.of("ccTypes");
				
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, countReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_cccard", TOTAL_NO_OF_CC_BY_TYPE, aggregateOptions);
		System.out.println("*********** Total no of credit card by type *******************");
		for (Map<String, Object> map : results) {
			Set<Entry<String, Object>> entrySet = map.entrySet();
			Iterator<Entry<String, Object>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, Object> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		System.out.println("********************************************************************************************\n");
	}
	
	
	private void getTotalNoOfInactiveCC(RediSearchCommands<String, String> commands) {
		Collection<String> groupByField = Arrays.asList(new String[] { "active" });
		Count countReducer = Reducer.Count.of("inactiveCards");
				
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, countReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_cccard", TOTAL_NO_OF_INACTIVE_CC, aggregateOptions);
		System.out.println("*********** Total no of inactive credit cards *******************");
		for (Map<String, Object> map : results) {
			Set<Entry<String, Object>> entrySet = map.entrySet();
			Iterator<Entry<String, Object>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, Object> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		System.out.println("********************************************************************************************\n");
	}

}
