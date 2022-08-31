package com.bestarch.demo.domain;

import lombok.Data;

@Data
public class CreditCard {
	
	private String cif;
	private String description;
	private String creditCardNo;
	private String issueDate;
	private String expiryDate;
	private String cvv;
	private String type;
	private Boolean active;

}
