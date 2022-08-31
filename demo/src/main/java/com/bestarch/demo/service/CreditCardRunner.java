package com.bestarch.demo.service;

import java.util.Arrays;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

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
	private final static String QUERY = "@cif:(QEOE110093342)";

	@Override
	public void run(String... args) throws Exception {
		RediSearchCommands<String, String> commands = connection.sync();
		SearchOptions<String> searchOptions = SearchOptions.<String>builder()
				.returnFields(Arrays.asList(new String[] { "creditCardNo", "type" })).build();
		
		SearchResults<String, String> results = commands.search("idx_cccard", QUERY, searchOptions);

		for (Document<String, String> doc : results) {
			Set<Entry<String, String>> entrySet = doc.entrySet();
			Iterator<Entry<String, String>> iter = entrySet.iterator();
			while (iter.hasNext()) {
				Entry<String, String> en = iter.next();
				System.out.println(en.getKey() + " = " + en.getValue());
			}
		}
		System.out.println("********************************************************************************************");
	}

}
