#!/usr/bin/perl

use strict;
use warnings;

use Test::More;
use FindBin qw($Bin);
use lib "$Bin/..";
use test_helper;

use Slim::Utils::Log qw(logger logWarning logError);

subtest 'logger' => sub {
    my $log = logger('test_category');
    ok(defined($log), 'logger returns defined object');
    isa_ok($log, 'Log::Log4perl::Logger');
};

subtest 'logWarning' => sub {
    # Initialize the class to set $rootLogger
    Slim::Utils::Log->init({});
    
    eval { logWarning('test warning') };
    ok(!$@, 'logWarning did not die');
};

done_testing();
