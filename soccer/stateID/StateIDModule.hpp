// kate: indent-mode cstyle; indent-width 4; tab-width 4; space-indent false;
// vim:ai ts=4 et
#pragma once

#include <framework/Module.hpp>

/** Semantic State Identification system */
namespace StateIdentification
{
	class StateIDModule : public Module
	{
		public:
			typedef boost::shared_ptr<StateIDModule> shared_ptr;
			StateIDModule(SystemState *state);
			~StateIDModule();
			
			virtual void run();
		
		protected:
			SystemState *_state;

			// Utility functions for each of the general parameters

			/** Generates a new possession state from the current one */
			Packet::LogFrame::Possession updatePossession(const Packet::LogFrame::Possession& cur_state);

			/** Determines the ball field position - with hysteresis */
			Packet::LogFrame::BallFieldPos updateFieldPos(const Packet::LogFrame::BallFieldPos& cur_pos);
	};
}