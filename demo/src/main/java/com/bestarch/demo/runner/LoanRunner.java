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
import com.redislabs.lettusearch.AggregateOptions.Operation.GroupBy.Reducer.Max;
import com.redislabs.lettusearch.AggregateOptions.Operation.GroupBy.Reducer.Sum;
import com.redislabs.lettusearch.AggregateResults;
import com.redislabs.lettusearch.RediSearchCommands;
import com.redislabs.lettusearch.StatefulRediSearchConnection;

@Component
@Order(3)
public class LoanRunner implements CommandLineRunner {
	
	@Autowired
	private StatefulRediSearchConnection<String, String> connection;
	
	//FT.AGGREGATE idx_loan '@amount:[0 +inf]' groupby 1 @loanType REDUCE MAX 1 @amount as loanmount 
	private final static String MAXIMUM_LOAN_BY_LOANTYPE = "@amount:[0 +inf]";
	
	//FT.AGGREGATE idx_loan *  groupby 1 @loanType REDUCE SUM 1 @amount as loanmount
	private final static String TOTAL_LOAN_LIABILITY_BY_LOANTYPE = "*";
	
	//FT.AGGREGATE idx_loan '@loanType:{HOME}' groupby 1 @loanType  REDUCE SUM 1 @amount as loanmount
	private final static String TOTAL_LOAN_GIVEN_AS_HOME_LOAN = "@loanType:{HOME}";
	
	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		
		getMaximumLoanByLoanType(commands);
		getTotalLoanLiabilityByLoanType(commands);
		getTotalLoanGivenAsHomeLoan(commands);
	}

	private void getMaximumLoanByLoanType(RediSearchCommands<String, String> commands) {
		Collection<String> groupByField = Arrays.asList(new String[] { "loanType" });
		Max maxReducer = Reducer.Max.builder()
				.property("amount").as("loanmount")
				.build();
		
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, maxReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_loan", MAXIMUM_LOAN_BY_LOANTYPE, aggregateOptions);
		System.out.println("*********** Maximum loan by loan type *******************");
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
	
	private void getTotalLoanLiabilityByLoanType(RediSearchCommands<String, String> commands) {
		Collection<String> groupByField = Arrays.asList(new String[] { "loanType" });
		Sum sumReducer = Reducer.Sum.builder()
				.property("amount").as("loanmount")
				.build();
		
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, sumReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_loan", TOTAL_LOAN_LIABILITY_BY_LOANTYPE, aggregateOptions);
		System.out.println("*********** Total loan liability by loan type *******************");
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
	
	private void getTotalLoanGivenAsHomeLoan(RediSearchCommands<String, String> commands) {
		Collection<String> groupByField = Arrays.asList(new String[] { "loanType" });
		Sum sumReducer = Reducer.Sum.builder()
				.property("amount").as("loanmount")
				.build();
		
		AggregateOptions aggregateOptions = AggregateOptions.builder()
									.groupBy(groupByField, sumReducer)
									.build();
		AggregateResults<String> results = commands.aggregate("idx_loan", TOTAL_LOAN_GIVEN_AS_HOME_LOAN, aggregateOptions);
		System.out.println("*********** Total loan given as home loan *******************");
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
