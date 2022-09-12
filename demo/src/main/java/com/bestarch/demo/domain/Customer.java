package com.bestarch.demo.domain;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class Customer {

	private String cif;
	private String bankCode;
	private String ifsc;
	private String email;
	private String name;
	private String address;
	private String virtualVault;
	private String phone;
	private String mobile;
	private String pan;
	private String aadhaar;
	private String dob;
	private Boolean kycOnfile;

}
