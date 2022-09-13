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
import com.redis.lettucemod.search.Group;
import com.redis.lettucemod.search.Reducers;
import com.redis.lettucemod.search.Reducers.Max;
import com.redis.lettucemod.search.Reducers.Sum;

@Component
@Order(3)
public class LoanRunner implements CommandLineRunner {
	
	private static Logger logger = LoggerFactory.getLogger(LoanRunner.class);
	
	@Autowired
	private StatefulRedisModulesConnection<String, String> connection;
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_loan '@amount:[0 +inf]' groupby 1 @loanType REDUCE MAX 1 @amount as loanmount 
	 */
	private final static String MAXIMUM_LOAN_BY_LOANTYPE = "@amount:[0 +inf]";
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_loan *  groupby 1 @loanType REDUCE SUM 1 @amount as loanmount
	 */
	private final static String TOTAL_LOAN_LIABILITY_BY_LOANTYPE = "*";
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_loan '@loanType:{HOME}' groupby 1 @loanType  REDUCE SUM 1 @amount as loanmount
	 */
	private final static String TOTAL_LOAN_GIVEN_AS_HOME_LOAN = "@loanType:{HOME}";
	
	@Override
	public void run(String... args) throws Exception {
		getMaximumLoanByLoanType();
		getTotalLoanLiabilityByLoanType();
		getTotalLoanGivenAsHomeLoan();
	}

	private void getMaximumLoanByLoanType() {
		RediSearchCommands<String, String> commands = connection.sync();
		
		Max maxReducer = Reducers.Max
				.property("amount").as("loanmount")
				.build();
		
		Group group = Group
				.by(new String[] { "loanType" })
				.reducer(maxReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_loan", MAXIMUM_LOAN_BY_LOANTYPE, aggregateOptions);
		
		logger.info("*********** Maximum loan by loan type *******************");
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
	
	private void getTotalLoanLiabilityByLoanType() {
		RediSearchCommands<String, String> commands = connection.sync();
		Sum sumReducer = Reducers.Sum
				.property("amount").as("loanmount")
				.build();
		
		Group group = Group
				.by(new String[] { "loanType" })
				.reducer(sumReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_loan", TOTAL_LOAN_LIABILITY_BY_LOANTYPE, aggregateOptions);
		logger.info("*********** Total loan liability by loan type *******************");
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
	
	private void getTotalLoanGivenAsHomeLoan() {
		RediSearchCommands<String, String> commands = connection.sync();
		Sum sumReducer = Reducers.Sum
				.property("amount").as("loanmount")
				.build();
		
		Group group = Group
				.by(new String[] { "loanType" })
				.reducer(sumReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_loan", TOTAL_LOAN_GIVEN_AS_HOME_LOAN, aggregateOptions);
		
		logger.info("*********** Total loan given as home loan *******************");
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
