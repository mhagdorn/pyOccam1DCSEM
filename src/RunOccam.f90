!=======================================================================
! Occam's Inversion Fortran2003 Code 
!=======================================================================
!
!    Copyright (C) 1986-2016
!    Steven Constable, Kerry Key, David Myer, Catherine deGroot-Hedlin
!    Scripps Institution of Oceanography
!    University of California, San Diego
!
!    This file is part of Occam's Inversion.
!
!    Occam's Inversion is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    Occam's Inversion is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with Occam's Inversion.  If not, see <http://www.gnu.org/licenses/>.
!
!-----------------------------------------------------------------------
!
! This file is a routine to run Occam's inversion.  
! It calls module Occam in file Occam.f90 for computing 
! each Occam iteration and for performing Occam I/O.
!
! For extensive Occam programming notes, see top of file Occam.f90.
!
!-----------------------------------------------------------------------
    program runOccam
!-----------------------------------------------------------------------

    ! Modules to include:
    use Occam 
 
    implicit none
      

! local variables:
    integer  :: maxitr, itmax, konv, ifftol, n
!   lerr = error flag for file operations
!   maxitr = maximum number of subsequent iterations by this run
!   itmax = maximum iteration number
!   konv = convergence flag from OCCAM
!   ifftol = convergence info from OCCAM (has the desired misfit been achieved?)
    real(RealPrec) :: tolreq, tobt, pmu, stepsz, rlast
!   tolreq = desired misfit, in RMS standard errors
!   tobt = current misfit
!   pmu = current Lagrange multiplier
!   stepsz = current RMS step through model space
!   rlast = last RMS measure of roughness
    character(50) :: descr,  cStartup ='startup'
!   descr = description line in iteration files
!   cStartup = name of starting file.  (See notes below)

    logical   :: bFwdOnly = .false.
!   bFwdOnly = set true if -F on cmd line ... saying to produce a fwd model & exit.
    logical :: lrunOccam
!   lrunOccam = .true. to run the occam iterations.  Some compilers do not
!     like looping over a static .true.


    real(8) :: timeOffset ! Timer temp:
    real(8) :: time0      ! Start time of Occam program (in seconds)
    real(8) :: timeIter0  ! Start time of an Occam iteration 
    
    ! For the AutoConverge feature - need to track misfit in ALL iterations
    real(RealPrec), dimension(:), allocatable :: rTrackMisfit

!-----------------------------------------------------------------------

!
! Start the timer:
!
    call get_time_offset(0d0, time0)

    write(*,*) ' ' 
    write(*,*) '------------------------------------------------------------'
    write(*,*) ' Occam''s Inversion              Version 3.15, March 2, 2016'
    write(*,*) ' ' 
    write(*,*) ' Original Reference: '
    write(*,*) ''
    write(*,*) ' Constable, S. C., R. L. Parker, and C. G. Constable, 1987, '
    write(*,*) ' Occam''s inversion - A practical algorithm for generating   '
    write(*,*) ' smooth models from electromagnetic sounding data, '
    write(*,*) ' Geophysics, 52, 289-300. '
    write(*,*) ' '
    write(*,*) ' Copyright (C) 1986-2016'
    write(*,*) ' Steven Constable, Kerry Key, David Myer, Catherine deGroot-Hedlin'
    write(*,*) ' Scripps Institution of Oceanography'
    write(*,*) ' University of California, San Diego'
    write(*,*) ' '
    write(*,*) ' License: '
    write(*,*) ' '
    write(*,*) ' Occam''s Inversion is free software: you can redistribute it and/or modify'
    write(*,*) ' it under the terms of the GNU General Public License as published by'
    write(*,*) ' the Free Software Foundation, either version 3 of the License, or'
    write(*,*) ' (at your option) any later version.'
    write(*,*) ' '
    write(*,*) ' Occam''s Inversion is distributed in the hope that it will be useful,'
    write(*,*) ' but WITHOUT ANY WARRANTY; without even the implied warranty of'
    write(*,*) ' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the'
    write(*,*) ' GNU General Public License for more details.'
    write(*,*) '  '
    write(*,*) ' You should have received a copy of the GNU General Public License'
    write(*,*) ' along with Occam''s Inversion.  If not, see <http://www.gnu.org/licenses/>.'
    write(*,*) ' '
    write(*,*) '------------------------------------------------------------'
    write(*,*) ' '
    
     
    ! DGM Oct 2006 - look for a command line parameter telling the name of
    ! the startup file.  If not given, then use 'startup'.
    ! If two params are given, then first is the startup file and the 2nd
    ! is the root filename for output of iteration, response, & log files.
    ! KWK, Dec 2008:
    ! New code for getting command line arguments using Fortran2003 standard intrinsics 
    ! command_argument_count()  and get_command_argument()
    !
    call getOccamCommandLineArguments(cStartup,cRootName,bFwdOnly)
    write(*,*) ' Startup File: ', trim(cStartup)
    write(*,*) '    Root Name: ', trim(cRootName)
    

    ! Read in the startup file:
    ! (Startup and iteration files should be machine written, and so we do
    ! not necessarily test the validity of the input data unless arrays are 
    ! involved.)
    call readIteration (cStartup,descr,maxitr,tolreq, pmu,rlast,tobt,ifftol)
  
    ! Read in the data file:
    call readData
    
    ! Allocate things related to the number of data
    call allocateNdArrays
    
    ! Read in the model:
    call readModel

    ! Allocate working arrays for storing associated parameters if defined:
    call allocateAssocArrays
    
    ! If we are to produce a forward model only, do so & exit.
    if (bFwdOnly) then
        write(*,*) 'Outputting FORWARD MODEL ONLY...'
        
         if (lConstrainParams) then
             call computeFwd( .false., transformToBound(pm)) 
         else               
             call computeFwd( .false., pm)   ! KWK Sept 2008.  Output now done through model occam_interface_mod 
         endif

        
        ! Show the misfit
        rlast = sqrt(sum( ((D - DM)/SD)**2 )/nd )       ! Array math - stack alloc of only nd size
        
        write(*,*) ' Forward Model Response Misfit:', rlast
        
        ! write out the model response:
        if (trim(cRootName) == 'ITER') then
            ! Assign a default rootname:
            cRootName = cStartup ! just point to the startupfile
        endif
        call writeResponse() 
        write(*,*) ' '
        write(*,*) ' Done! '
        write(*,*) ' '
            
        
    else        ! Invert!
   
        ! Open a logfile:
        call openOccamLogFile()

        ! if this is zeroth iteration copy the startup file into ITER00
        if (nCurrentIter == 0) then
            ! initialize the inversion parameters
            pmu     = 5.0
            rlast   = 1.0e+10
            tobt    = 1000.0
            ifftol  = 0
            call writeIteration (descr,maxitr,tolreq,pmu,rlast,tobt,ifftol)
        end if

        itmax = maxitr + nCurrentIter
        write(*,*) 'Major I/O accomplished, sit back and relax.......'
        write(*,*) ' '

        ! For auto-convergence, need to keep track of misfit by iteration
        if( bAutoConv ) then
            allocate( rTrackMisfit(nCurrentIter + itmax) )
            if( nCurrentIter > 0 ) then  ! starting mid-stream, so keep the prev misfit
                rTrackMisfit = 1.0e+10   ! make em all too big to trigger auto-converge
                rTrackMisfit(nCurrentIter) = tobt
            endif
        end if
        
        lrunOccam= .true.
        
        ! Run the main loop
        do while (lrunOccam)
            
            ! Start the iteration timer:
            call get_time_offset( 0d0,timeIter0)
        
            ! Compute an Occam iteration:
            call compOccamIteration(tolreq,tobt,ifftol,pmu,rlast,stepsz,konv)
            
            ! DGM Feb 2011 Try something new for the konv=4 (auto-convergence
            ! based on delta misfit). Rather than ending, go ahead and set the
            ! system as converged and let smoothing iterations begin.
            if( konv == 4 ) then
                write(ioUnitOccamLogFile,*) 'Misfit changed by less than Delta Misfit Limit.'
                write(ioUnitOccamLogFile,*) 'Changing target and starting smoothing.'
                write(*,*) 'Misfit changed by less than Delta Misfit Limit.'
                write(*,*) 'Changing target and starting smoothing.'
                
                ifftol = 1
                tolreq = tobt
                konv   = 0      ! reset so we don't stop
                stepsz = 1      ! don't let previous teeny chg in model keep us from at least 1 smoothing iter
                
                ! But don't go on forever...
                if( itmax - nCurrentIter > 5 ) itmax = nCurrentIter + 5
            endif
            
            ! DGM Feb 2010 if the convergence code is 2 or 3, then the inversion
            ! is ending without converging.  In this case, dm (model response)
            ! is not guaranteed to be a realistic model.  It is sometimes set
            ! to something wild from the various minimizer routines searching
            ! desperately for a solution. Do NOT output this iteration & response
            ! because it is worthless anyway.  In these cases the rms misfit reported
            ! in the iteration file does not match what you can calculate from 
            ! the response file.
            if (.not.(konv == 2 .or. konv == 3)) then
                ! write an iteration output file:
                call writeIteration ( descr,maxitr,tolreq,pmu,rlast,tobt,ifftol )
                
                ! write out the model response:
                call writeResponse() 
            endif
            
            ! Display information to the terminal window:
            write(*,*) ' '
            write(*,*) ' ----------------------------------'
            write(*, '(a24,i8)') ' Iteration:', nCurrentIter
            write(*, '(a24,g12.4)') ' RMS Misfit:', tobt
            if (ifftol == 1) then
                write(*, '(a24,g12.4,a9)') 'Target Misfit:', tolreq, ' reached!'
            else
                write(*, '(a24,g12.4)') 'Target Misfit:', tolreq
            endif
            write(*, '(a24,g12.4)') ' Roughness:', rlast
            write(*, '(a24,g12.4)') ' Stepsize:', stepsz
            call get_time_offset( timeIter0,timeOffset)
            write(*, '(a24,g12.4)') ' Iteration Time (s):', timeOffset
            call get_time_offset( time0,timeOffset)
            write(*, '(a24,g12.4)') ' Total Time (s):', timeOffset
            write(*,*) ' ----------------------------------'
            write(*,*) ' '

            ! test for convergence: continue inversion if 
            !   1) iteration number does not exceed maximum, and
            !   2) stepsize is still significant, and
            !   3) rms misfit larger than required, and 
            !   4) there are no irrecoverable convergence problems
            if (konv .ne. 0) then
                select case (konv)
                case (1)
                    write(ioUnitOccamLogFile,*)   'Perfectly smooth model found.'
                    write(*,*)      'Perfectly smooth model found.'
                case (2)
                    write(ioUnitOccamLogFile,*)   'Convergence problems from RMS Misfit'
                    write(*,*)      'Convergence problems from RMS Misfit'
                    write(*,*)      'May have reached minimum possible RMS Misfit level!'
                    
                    if( bAutoConv .and. bAConkonvEq2 ) then
                        rTrackMisfit(nCurrentIter) = tobt
                        tolreq = rTrackMisfit(nCurrentIter) * rAC_Factor
!                        ifftol = 1
! DGM 8/2011 - don't set the flag, let the next iteration back off by itself
                        bAutoConv = .false.
                        
                        write(*,*) ' -------------------------------------------------'
                        write(*,*) ' AUTO CONVERGENCE TRIGGERED by Convergence problem'
                        write(*,'(A,F10.5,A)') ' New Target = ', tolreq ! , ' reached!'
                        write(*,*) ' -------------------------------------------------'
                        write(ioUnitOccamLogFile,*) ' -------------------------------------------------'
                        write(ioUnitOccamLogFile,*) ' AUTO CONVERGENCE TRIGGERED by Convergence problem'
                        write(ioUnitOccamLogFile,*) ' New Target = ', tolreq  !, ' reached!'
                        write(ioUnitOccamLogFile,*) ' -------------------------------------------------'

                        ! write an iteration output file:
                        call writeIteration ( descr,maxitr,tolreq,pmu,rlast,tobt,ifftol )
                        
                        ! write out the model response:
                        call writeResponse() 
                        
                        cycle
                    endif
                case (3)
                    write(ioUnitOccamLogFile,*)   'Convergence problems from Smoothness'
                    write(*,*)      'Convergence problems from Smoothness'
                    write(*,*)      'May have reached minimum possible RMS Misfit level!'
                case (4)
                    write(ioUnitOccamLogFile,*)   'Misfit changed by less than Delta Misfit Limit.'
                    write(*,*)      'Misfit changed by less than Delta Misfit Limit.'
                    write(*,*)      'Stopping inversion so you can check the data to see'
                    write(*,*)      'if the error level needs to be adjusted or if some'
                    write(*,*)      'data points need to be removed.'
                case default
                    write(ioUnitOccamLogFile,*)   ' Convergence problems of type ', konv
                    write(*,*)      ' Convergence problems of type ', konv
                end select
                close(ioUnitOccamLogFile)
                exit
                
            else if (nCurrentIter >= itmax) then
            ! Inversion has reached max # of iterations specified in startup file.
            !   Stop now even if not converged.
            ! NOTE: This check MUST be before the "continue" check below.
                write(ioUnitOccamLogFile,*) ' Stop on maximum iterations'
                close(ioUnitOccamLogFile)
                write(*,*) ' Reached maximum iterations.  Done.'
                exit
                
            else if ((tobt < 1.01*tolreq) .and. (stepsz < 0.001)) then
                write(ioUnitOccamLogFile,*) ' Stop on normal convergence'
                close(ioUnitOccamLogFile)
                write(*,*) ' Solution converged!  Done.'
                exit
            !    
            ! else... continue...    
            
            end if
            
            ! Look for auto-convergence (DGM 12/2010)
            if( bAutoConv .and. ifftol == 0 ) then
                rTrackMisfit(nCurrentIter) = tobt
                if( nCurrentIter-iAC_IterCnt > 0 ) then
                    if( rTrackMisfit(nCurrentIter-iAC_IterCnt) &
                      - rTrackMisfit(nCurrentIter) &
                        < rAC_Threshold) then
                        
!                        ifftol = 1
! DGM 8/2011 - don't set the flag, let the next iteration back off by itself
                        tolreq = rTrackMisfit(nCurrentIter) * rAC_Factor
                        bAutoConv = .false.
                        
                        write(*,*) ' ------------------------------'
                        write(*,*) ' AUTO CONVERGENCE TRIGGERED'
                        write(*,'(A,F10.5,A)') ' New Target = ', tolreq ! , ' reached!'
                        write(*,*) ' ------------------------------'
                        write(ioUnitOccamLogFile,*) ' ------------------------------'
                        write(ioUnitOccamLogFile,*) ' AUTO CONVERGENCE TRIGGERED'
                        write(ioUnitOccamLogFile,*) ' New Target = ', tolreq ! , ' reached!'
                        write(ioUnitOccamLogFile,*) ' ------------------------------'
                    
                    end if
                end if
            end if
            
        enddo
    endif
    
    ! Deallocate memory & return control to the user
    call deallocateOccam
    
    if( bAutoConv ) deallocate( rTrackMisfit, stat=n )

end program runOccam
