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
import com.redis.lettucemod.search.Reducers.Count;

@Component
@Order(4)
public class AccountRunner implements CommandLineRunner {
	
	private static Logger logger = LoggerFactory.getLogger(AccountRunner.class);
	
	@Autowired
	private StatefulRedisModulesConnection<String, String> connection;
	
	/**
	 * Actual RediSearch query --> 
	 * FT.AGGREGATE idx_account * groupBy 1 @accountType REDUCE COUNT 0 as count
	 */
	private final static String NUMBER_OF_TYPES_OF_ACCOUNT_PRESENT_IN_BANK = "*";
	
	@Override
	public void run(String... args) throws Exception {
		getNoOfTypesOfAccountPresentInBank();
	}

	private void getNoOfTypesOfAccountPresentInBank() {
		RediSearchCommands<String, String> commands = connection.sync();
		
		Count countReducer = Reducers.Count.as("count");
		
		Group group = Group
				.by(new String[] { "accountType" })
				.reducer(countReducer)
				.build();
		
		AggregateOptions<String, String> aggregateOptions = AggregateOptions.<String, String>builder()
				.operation(group)
				.build();
		
		AggregateResults<String> results = commands.ftAggregate("idx_account", NUMBER_OF_TYPES_OF_ACCOUNT_PRESENT_IN_BANK, aggregateOptions);
		
		logger.info("*********** No of types of account held in bank *******************");
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
