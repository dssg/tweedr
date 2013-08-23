# Extraction Tool

This tool can be used to create labeled data from tweets. 

## Setup Database for tweet output
CREATE TABLE `tokenized_labels` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `dssg_id` int(100) NOT NULL,
  `tweet` varchar(500) DEFAULT NULL,
  `token_start` int(50) DEFAULT NULL,
  `token_end` int(50) DEFAULT NULL,
  `token_type` varchar(500) DEFAULT NULL,
  `token` varchar(500) DEFAULT NULL,
  `mturk_code` varchar(50) DEFAULT NULL,
  `which_sample` varchar(10) DEFAULT NULL,
  `which_disaster` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=908 DEFAULT CHARSET=latin1;


## Contact

Want to get in touch? Found a bug? Open up a [new issue](https://github.com/dssg/tweedr/issues/new) or email us at [dssg-qcri@googlegroups.com](mailto:dssg-qcri@googlegroups.com).


## License

Copyright © 2013 The University of Chicago. [MIT Licensed](LICENSE).
