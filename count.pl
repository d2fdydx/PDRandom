#!/usr/bin/env perl

my $temp;
my @temp;
my $sum;
while(<>){
	@temp=split(/\s+/,$_);
	$temp=$temp[-1];
	$sum+=$temp;

}
print $sum;