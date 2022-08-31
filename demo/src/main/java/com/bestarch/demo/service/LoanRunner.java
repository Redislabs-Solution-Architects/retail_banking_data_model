package com.bestarch.demo.service;

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
import com.redislabs.lettusearch.AggregateOptions.Operation.GroupBy.Reducer.Max;
import com.redislabs.lettusearch.AggregateResults;
import com.redislabs.lettusearch.RediSearchCommands;
import com.redislabs.lettusearch.StatefulRediSearchConnection;

@Component
@Order(3)
public class LoanRunner implements CommandLineRunner {
	
	@Autowired
	private StatefulRediSearchConnection<String, String> connection;
	
	//FT.AGGREGATE idx_loan '@amount:[0 +inf]' groupby 1 @loanType REDUCE MAX 1 @amount as loanmount 
	private final static String QUERY = "@amount:[0 +inf]";
	
	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		
		Collection<String> groupByField = Arrays.asList(new String[] { "loanType" });
		Max maxReducer = Reducer.Max.builder()
				.property("amount").as("loanmount")
				.build();
		
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, maxReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_loan", QUERY, aggregateOptions);
		
		for (Map<String, Object> map : results) {
			Set<Entry<String, Object>> entrySet = map.entrySet();
			Iterator<Entry<String, Object>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, Object> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		System.out.println("********************************************************************************************");
	}

}
