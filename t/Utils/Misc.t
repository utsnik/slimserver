#!/usr/bin/perl

use strict;
use warnings;

use Test::More;
use FindBin qw($Bin);
use lib "$Bin/..";
use test_helper;

use Slim::Utils::Misc qw(msg);

subtest 'msg' => sub {
    ok(defined(&msg), 'msg function is defined');
    
    # Simple call test
    eval { msg("Test message\n") };
    ok(!$@, 'msg call did not die: $@');
};

done_testing();
