package test_helper;

use strict;
use warnings;
use FindBin qw($Bin);
use File::Spec;

# Add server root to the front
use lib File::Spec->catdir($Bin, '..', '..');

# Add bundled CPAN to the BACK of @INC to avoid shadowing system modules like Test::More
BEGIN {
    my $cpan_dir = File::Spec->catdir($Bin, '..', '..', 'CPAN');
    push @INC, $cpan_dir;
}

# Mock dependencies to allow loading in an environment without LMS binaries
BEGIN {
    # Define constants in main
    {
        no strict 'refs';
        *main::ISWINDOWS = sub { 0 };
        *main::DEBUGLOG  = sub { 0 };
        *main::INFOLOG   = sub { 0 };
        *main::SCANNER   = sub { 0 };
        *main::RESIZER   = sub { 0 };
        *main::TRANSCODING = sub { 0 };
        *main::STATISTICS = sub { 0 };
        *main::SB1SLIMP3SYNC = sub { 0 };
        *main::WEBUI = sub { 0 };
        *main::ISMAC = sub { 0 };
        *main::NOMYSB = sub { 1 };
        *main::PERFMON = sub { 0 };
        *main::ISUNIX = sub { 1 };
        *main::REVISION = sub { "9.1.0" };
        *main::idleStreams = sub { };
    }

    # Mock Log4perl (External Dependency)
    $INC{'Log/Log4perl.pm'} = 1;
    $INC{'Log/Log4perl/Logger.pm'} = 1;
    $INC{'Log/Log4perl/Appender/Screen.pm'} = 1;
    $INC{'Log/Log4perl/Appender/File.pm'} = 1;
    {
        package Log::Log4perl::Logger;
        sub new { return bless {}, shift }
        sub get_logger { return Log::Log4perl::Logger->new() }
        sub error { }
        sub warn { }
        sub info { }
        sub debug { }
        sub is_debug { return 0 }
        sub is_info { return 0 }
        
        package Log::Log4perl;
        sub init { }
        sub get_logger { return Log::Log4perl::Logger->new() }
        sub initialized { return 1 }
    }

    # Mock Prefs (Complex Subsystem)
    $INC{'Slim/Utils/Prefs.pm'} = 1;
    {
        package Slim::Utils::Prefs;
        sub preferences { return bless {}, 'MockPrefs' }
        
        package MockPrefs;
        sub get { return "" }
        sub set { }
        sub setChange { }
        
        # Global import mock for modules that import it
        *Slim::Utils::Log::preferences = \&Slim::Utils::Prefs::preferences;
        *Slim::Utils::Misc::preferences = \&Slim::Utils::Prefs::preferences;
        *Slim::Utils::Strings::preferences = \&Slim::Utils::Prefs::preferences;
    }

    # Mock OSDetect (Complex Subsystem)
    $INC{'Slim/Utils/OSDetect.pm'} = 1;
    {
        package Slim::Utils::OSDetect;
        sub getOS { return bless {}, 'MockOS' }
        sub OS { return 'unix' }
        sub details { return { osArch => 'x86_64' } }
        sub dirsFor { return "." }
        
        package MockOS;
        sub logRotate { }
        sub ignoredItems { return () }
    }

    # Mock Binary Helpers
    $INC{'Digest/SHA1.pm'} = 1;
    {
        package Digest::SHA1;
        use Exporter::Lite;
        our @EXPORT_OK = qw(sha1_hex);
        sub sha1_hex { return "mock_sha1" }
    }

    $INC{'JSON/XS.pm'} = 1;
    $INC{'JSON/XS/VersionOneAndTwo.pm'} = 1;
    {
        package JSON::XS;
        sub to_json { return "{}" }
        sub from_json { return {} }
        package JSON::XS::VersionOneAndTwo;
        # Already covered by JSON::XS often in LMS
    }

    # Mock other requirements that usually fail or require binaries
    $INC{'Slim/Music/Info.pm'} = 1;
    $INC{'Slim/Player/ProtocolHandlers.pm'} = 1;
    $INC{'Slim/Utils/Unicode.pm'} = 1;
    $INC{'Slim/Utils/PluginManager.pm'} = 1;
    $INC{'Slim/Utils/DateTime.pm'} = 1;
    $INC{'Slim/Networking/SimpleAsyncHTTP.pm'} = 1;
    $INC{'Slim/Networking/Async/HTTP.pm'} = 1;
    
    {
        package Slim::Utils::PluginManager;
        sub dirsFor { return () }
        
        package Slim::Utils::DateTime;
        sub new { return bless {}, shift }
    }
}

1;
